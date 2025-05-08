import unittest
from typing import Optional

import paddle

from src.networks.net_utils import MLP
from src.networks.warp_search import NeighborSearchReturnType
from src.networks.warp_search import radius_search_warp as FixedRadiusSearch

# import open3d
# from open3d.ml.paddle.layers import FixedRadiusSearch
# FixedRadiusSearch = FixedRadiusSearch()
# NeighborSearchReturnType = (
#     open3d.ml.paddle.python.return_types.open3d_fixed_radius_search
# )


def segment_mean_csr(src: paddle.Tensor, indptr: paddle.Tensor, out):
    num_seg = indptr.shape[0] - 1
    belongs_to = paddle.arange(num_seg)
    repeats = indptr[1:] - indptr[:-1]
    belongs_to = paddle.repeat_interleave(
        belongs_to,
        repeats,
    )
    res = paddle.geometric.segment_mean(src, belongs_to)

    if res.shape[0] < num_seg:
        zero = paddle.zeros([num_seg - res.shape[0], res.shape[1]])
        res = paddle.concat([res, zero], axis=0)
    res = paddle.reshape(res, [num_seg, res.shape[1]])
    return res


def segment_sum_csr(src: paddle.Tensor, indptr: paddle.Tensor, out):
    num_seg = indptr.shape[0] - 1
    belongs_to = paddle.arange(num_seg)
    repeats = indptr[1:] - indptr[:-1]
    belongs_to = paddle.repeat_interleave(
        belongs_to,
        repeats,
    )
    res = paddle.geometric.segment_sum(src, belongs_to)

    if res.shape[0] < num_seg:
        zero = paddle.zeros([num_seg - res.shape[0], res.shape[1]])
        res = paddle.concat([res, zero], axis=0)
    res = paddle.reshape(res, [num_seg, -1])
    return res


def segment_csr(
    src: paddle.Tensor,
    indptr: paddle.Tensor,
    out: Optional[paddle.Tensor] = None,
    reduce: str = "sum",
) -> paddle.Tensor:
    if reduce == "mean":
        return segment_mean_csr(src, indptr, out)
    elif reduce == "sum":
        return segment_sum_csr(src, indptr, out)
    else:
        raise NotImplementedError


class NeighborSearchLayer(paddle.nn.Layer):
    def __init__(self, radius: float):
        super().__init__()
        self.radius = radius
        self.nsearch = FixedRadiusSearch

    def forward(
        self, inp_positions: paddle.Tensor, out_positions: paddle.Tensor
    ) -> NeighborSearchReturnType:
        paddle.device.synchronize()
        neighbors = self.nsearch(inp_positions, out_positions, self.radius)
        paddle.device.synchronize()
        return neighbors


class NeighborPoolingLayer(paddle.nn.Layer):
    def __init__(self, reduction="mean"):
        super().__init__()
        self.reduction = reduction

    def forward(
        self, in_features: paddle.Tensor, neighbors: NeighborSearchReturnType
    ) -> paddle.Tensor:
        rep_features = in_features[neighbors.neighbors_index.astype(paddle.int64)]
        out_features = segment_csr(
            rep_features, neighbors.neighbors_row_splits, reduce=self.reduction
        )
        return out_features


class NeighborMLPConvLayer(paddle.nn.Layer):
    def __init__(
        self, mlp=None, in_channels=8, hidden_dim=32, out_channels=32, reduction="mean"
    ):
        super().__init__()
        self.reduction = reduction
        if mlp is None:
            mlp = MLP([2 * in_channels, hidden_dim, out_channels], paddle.nn.GELU)
        self.mlp = mlp

    def forward(
        self,
        in_features: paddle.Tensor,
        neighbors: NeighborSearchReturnType,
        out_features: Optional[paddle.Tensor] = None,
    ) -> paddle.Tensor:
        """
        inp_features: [N,C]
        outp_features: [M,C]
        neighbors: ml3d.layers.FixedRadiusSearchResult.
        """
        if out_features is None:
            out_features = in_features
        assert (
            in_features.shape[1] + out_features.shape[1]
            == self.mlp.layers[0].weight.shape[0]
        )
        rep_features = in_features[neighbors.neighbors_index.astype(paddle.int64)]
        rs = neighbors.neighbors_row_splits
        num_reps = rs[1:] - rs[:-1]

        self_features = paddle.repeat_interleave(
            x=out_features, repeats=num_reps, axis=0
        )
        agg_features = paddle.concat(x=[rep_features, self_features], axis=1)
        rep_features = self.mlp(agg_features)
        out_features = segment_csr(
            rep_features,
            neighbors.neighbors_row_splits,
            reduce=self.reduction,
        )
        return out_features


class NeighborMLPConvLayerWeighted(paddle.nn.Layer):
    def __init__(
        self, mlp=None, in_channels=8, hidden_dim=32, out_channels=32, reduction="mean"
    ):
        super().__init__()
        self.reduction = reduction
        if mlp is None:
            mlp = MLP([2 * in_channels, hidden_dim, out_channels], paddle.nn.GELU)
        self.mlp = mlp

    def forward(
        self,
        in_features: paddle.Tensor,
        neighbors: NeighborSearchReturnType,
        out_features: Optional[paddle.Tensor] = None,
        in_weights: Optional[paddle.Tensor] = None,
    ) -> paddle.Tensor:
        """
        in_features: [N,C]
        out_features: [M,C]
        in_weights: [N]
        neighbors: ml3d.layers.FixedRadiusSearchResult.
        """
        if out_features is None:
            out_features = in_features

        assert (
            in_features.shape[1] + out_features.shape[1]
            == self.mlp.layers[0].weight.shape[0]
        )
        rep_features = in_features[neighbors.neighbors_index.astype(paddle.int64)]
        if in_weights is None:
            rep_weights = 1
        else:
            rep_weights = in_weights[
                neighbors.neighbors_index.astype(paddle.int64)
            ].unsqueeze(axis=-1)

        # sum first and then mlp to make cuda memory usage only related to grid shape
        rep_csr = segment_csr(
            rep_features, neighbors.neighbors_row_splits, reduce=self.reduction
        )
        del rep_features  # remove intermediate variables
        agg_csr = paddle.concat([rep_csr, out_features], axis=1)
        del rep_csr
        weights_csr = segment_csr(
            rep_weights, neighbors.neighbors_row_splits, reduce=self.reduction
        )
        del rep_weights
        out_features = weights_csr * self.mlp(agg_csr)

        return out_features


class NeighborMLPConvLayerLinear(paddle.nn.Layer):
    def __init__(
        self, mlp=None, in_channels=8, hidden_dim=32, out_channels=32, reduction="mean"
    ):
        super().__init__()
        self.reduction = reduction
        if mlp is None:
            mlp = MLP([2 * in_channels, hidden_dim, out_channels], paddle.nn.GELU)
        self.mlp = mlp

    def forward(
        self,
        x_in: paddle.Tensor,
        neighbors: NeighborSearchReturnType,
        in_features: paddle.Tensor,
        x_out: Optional[paddle.Tensor] = None,  # M = n_eval, N = x_in_chunks[j]
    ) -> paddle.Tensor:
        """
        inp_features: [N,C]
        outp_features: [M,C]
        neighbors: ml3d.layers.FixedRadiusSearchResult.
        """
        if x_out is None:
            x_out = x_in
        assert x_in.shape[1] + x_out.shape[1] == self.mlp.layers[0].weight.shape[0]

        rep_features = x_in[neighbors.neighbors_index.astype(paddle.int64)]
        in_features = in_features[neighbors.neighbors_index.astype(paddle.int64)]
        rs = neighbors.neighbors_row_splits
        num_reps = rs[1:] - rs[:-1]
        self_features = paddle.repeat_interleave(x=x_out, repeats=num_reps, axis=0)
        agg_features = paddle.concat(x=[rep_features, self_features], axis=1)
        rep_features = self.mlp(agg_features)
        rep_features = rep_features * in_features

        out_features = segment_csr(
            rep_features,
            neighbors.neighbors_row_splits,
            reduce=self.reduction,
        )
        return out_features


if __name__ == "__main__":
    unittest.main()
