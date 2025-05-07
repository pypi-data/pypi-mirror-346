# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING
from typing_extensions import override

if TYPE_CHECKING:
    from .resources.account import AccountResource
    from .resources.hardware import HardwareResource
    from .resources.trainings import TrainingsResource
    from .resources.collections import CollectionsResource
    from .resources.predictions import PredictionsResource
    from .resources.models.models import ModelsResource
    from .resources.webhooks.webhooks import WebhooksResource
    from .resources.deployments.deployments import DeploymentsResource

from . import _load_client
from ._utils import LazyProxy


class ModelsResourceProxy(LazyProxy["ModelsResource"]):
    @override
    def __load__(self) -> ModelsResource:
        return _load_client().models


class AccountResourceProxy(LazyProxy["AccountResource"]):
    @override
    def __load__(self) -> AccountResource:
        return _load_client().account


class HardwareResourceProxy(LazyProxy["HardwareResource"]):
    @override
    def __load__(self) -> HardwareResource:
        return _load_client().hardware


class WebhooksResourceProxy(LazyProxy["WebhooksResource"]):
    @override
    def __load__(self) -> WebhooksResource:
        return _load_client().webhooks


class TrainingsResourceProxy(LazyProxy["TrainingsResource"]):
    @override
    def __load__(self) -> TrainingsResource:
        return _load_client().trainings


class CollectionsResourceProxy(LazyProxy["CollectionsResource"]):
    @override
    def __load__(self) -> CollectionsResource:
        return _load_client().collections


class DeploymentsResourceProxy(LazyProxy["DeploymentsResource"]):
    @override
    def __load__(self) -> DeploymentsResource:
        return _load_client().deployments


class PredictionsResourceProxy(LazyProxy["PredictionsResource"]):
    @override
    def __load__(self) -> PredictionsResource:
        return _load_client().predictions


models: ModelsResource = ModelsResourceProxy().__as_proxied__()
account: AccountResource = AccountResourceProxy().__as_proxied__()
hardware: HardwareResource = HardwareResourceProxy().__as_proxied__()
webhooks: WebhooksResource = WebhooksResourceProxy().__as_proxied__()
trainings: TrainingsResource = TrainingsResourceProxy().__as_proxied__()
collections: CollectionsResource = CollectionsResourceProxy().__as_proxied__()
deployments: DeploymentsResource = DeploymentsResourceProxy().__as_proxied__()
predictions: PredictionsResource = PredictionsResourceProxy().__as_proxied__()
