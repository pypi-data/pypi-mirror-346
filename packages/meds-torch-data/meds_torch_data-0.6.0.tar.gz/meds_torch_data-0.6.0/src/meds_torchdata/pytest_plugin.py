"""This file exports pytest fixtures for static pytorch datasets for downstream testing use."""

import subprocess
import tempfile
from pathlib import Path

import pytest
from meds_testing_helpers.dataset import MEDSDataset

from meds_torchdata import MEDSPytorchDataset, MEDSTorchDataConfig
from meds_torchdata.extensions import _HAS_LIGHTNING


@pytest.fixture(scope="session")
def tensorized_MEDS_dataset(simple_static_MEDS: Path) -> Path:
    with tempfile.TemporaryDirectory() as cohort_dir:
        cohort_dir = Path(cohort_dir)

        command = [
            "MTD_preprocess",
            f"MEDS_dataset_dir={simple_static_MEDS!s}",
            f"output_dir={cohort_dir!s}",
        ]

        out = subprocess.run(" ".join(command), shell=True, check=False, capture_output=True)

        error_str = (
            f"Command failed with return code {out.returncode}.\n"
            f"Command stdout:\n{out.stdout.decode()}\n"
            f"Command stderr:\n{out.stderr.decode()}"
        )

        assert out.returncode == 0, error_str

        yield cohort_dir


@pytest.fixture(scope="session")
def tensorized_MEDS_dataset_with_task(
    tensorized_MEDS_dataset: Path,
    simple_static_MEDS_dataset_with_task: Path,
) -> tuple[Path, Path, str]:
    cohort_dir = tensorized_MEDS_dataset

    D = MEDSDataset(root_dir=simple_static_MEDS_dataset_with_task)

    if len(D.task_names) != 1:  # pragma: no cover
        raise ValueError("Expected only one task in the dataset.")

    yield cohort_dir, D.task_root_dir, D.task_names[0]


@pytest.fixture(scope="session")
def sample_dataset_config(tensorized_MEDS_dataset: Path) -> MEDSTorchDataConfig:
    config = MEDSTorchDataConfig(
        tensorized_cohort_dir=tensorized_MEDS_dataset,
        max_seq_len=10,
    )

    return config


@pytest.fixture(scope="session")
def sample_dataset_config_with_task(
    tensorized_MEDS_dataset_with_task: tuple[Path, Path, str],
) -> MEDSTorchDataConfig:
    cohort_dir, tasks_dir, task_name = tensorized_MEDS_dataset_with_task

    config = MEDSTorchDataConfig(
        tensorized_cohort_dir=cohort_dir,
        task_labels_dir=(tasks_dir / task_name),
        max_seq_len=10,
        seq_sampling_strategy="to_end",
    )

    return config


@pytest.fixture(scope="session")
def sample_pytorch_dataset(sample_dataset_config: MEDSTorchDataConfig) -> MEDSPytorchDataset:
    return MEDSPytorchDataset(sample_dataset_config, split="train")


@pytest.fixture(scope="session")
def sample_pytorch_dataset_with_task(
    sample_dataset_config_with_task: MEDSTorchDataConfig,
) -> MEDSPytorchDataset:
    return MEDSPytorchDataset(sample_dataset_config_with_task, split="train")


if _HAS_LIGHTNING:
    from meds_torchdata.extensions import Datamodule

    @pytest.fixture(scope="session")
    def sample_lightning_datamodule(sample_dataset_config: MEDSTorchDataConfig) -> Datamodule:
        return Datamodule(config=sample_dataset_config, batch_size=2)

    @pytest.fixture(scope="session")
    def sample_lightning_datamodule_with_task(
        sample_dataset_config_with_task: MEDSTorchDataConfig,
    ) -> Datamodule:
        return Datamodule(config=sample_dataset_config_with_task, batch_size=2)
