import paddle
from paddle.distributed import get_rank
from paddle.io import DistributedBatchSampler


class BaseDataModule:
    @property
    def train_dataset(self) -> paddle.io.Dataset:
        raise NotImplementedError

    @property
    def val_dataset(self) -> paddle.io.Dataset:
        raise NotImplementedError

    @property
    def test_dataset(self) -> paddle.io.Dataset:
        raise NotImplementedError

    def train_dataloader(self, enable_ddp=False, **kwargs) -> paddle.io.DataLoader:
        collate_fn = getattr(self, "collate_fn", None)
        if enable_ddp is True:
            sampler = DistributedBatchSampler(
                self.train_data, rank=get_rank(), batch_size=kwargs.get("batch_size", 1)
            )
            kwargs.pop("batch_size", None)
            return paddle.io.DataLoader(
                self.train_data, batch_sampler=sampler, collate_fn=collate_fn, **kwargs
            )
        else:
            return paddle.io.DataLoader(
                self.train_data, collate_fn=collate_fn, **kwargs
            )

    def val_dataloader(self, enable_ddp=False, **kwargs) -> paddle.io.DataLoader:
        collate_fn = getattr(self, "collate_fn", None)
        if enable_ddp is True:
            sampler = DistributedBatchSampler(
                self.val_data, rank=get_rank(), batch_size=1
            )
            return paddle.io.DataLoader(
                self.val_data, batch_sampler=sampler, collate_fn=collate_fn, **kwargs
            )
        else:
            return paddle.io.DataLoader(self.val_data, collate_fn=collate_fn, **kwargs)

    def test_dataloader(self, enable_ddp=False, **kwargs) -> paddle.io.DataLoader:
        collate_fn = getattr(self, "collate_fn", None)
        return paddle.io.DataLoader(self.test_data, collate_fn=collate_fn, **kwargs)
