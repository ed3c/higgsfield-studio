"""Explicit domain Managers; no manager can write another domain's artifacts."""
from .core import Factory, FactoryError, MANAGER_DOMAINS

class DomainManager:
    domain = ""
    def __init__(self, store: Factory):
        if self.domain not in MANAGER_DOMAINS:
            raise FactoryError("manager must own one domain")
        self.store = store
    def publish(self, namespace, key, uri, payload, *, expected_previous=None, derived_from=()):
        return self.store.publish(namespace=namespace, domain=self.domain,
            key=key, uri=uri, payload=payload,
            expected_previous=expected_previous, derived_from=derived_from)
    def send(self, project, consumer, asset_id, key, evidence):
        return self.store.handoff(project=project, producer=self.domain,
            consumer=consumer, asset_id=asset_id, key=key, evidence=evidence)
    def receive(self, event_id):
        return self.store.acknowledge(event_id, self.domain)

class PortfolioManager(DomainManager): domain="portfolio"
class ResearchManager(DomainManager): domain="research"
class StoryManager(DomainManager): domain="story"
class ArtDirectionManager(DomainManager): domain="art_direction"
class CharacterManager(DomainManager): domain="character"
class AssetManager(DomainManager): domain="asset"
class PromptManager(DomainManager): domain="prompt"
class ShotManager(DomainManager): domain="shot"
class OpticalManager(DomainManager): domain="optical"
class SoundManager(DomainManager): domain="sound"
class GenerationManager(DomainManager): domain="generation"
class BudgetManager(DomainManager): domain="budget"
class RightsManager(DomainManager): domain="rights"
class QCManager(DomainManager): domain="qc"
class DeliveryManager(DomainManager): domain="delivery"
class ProvenanceManager(DomainManager): domain="provenance"
class ExperimentManager(DomainManager): domain="experiment"

_MANAGER_CLASSES = {klass.domain: klass for klass in (
    PortfolioManager, ResearchManager, StoryManager, ArtDirectionManager,
    CharacterManager, AssetManager, PromptManager, ShotManager,
    OpticalManager, SoundManager, GenerationManager, BudgetManager,
    RightsManager, QCManager, DeliveryManager, ProvenanceManager,
    ExperimentManager
)}
assert set(_MANAGER_CLASSES) == set(MANAGER_DOMAINS)

def manager(name: str, store: Factory) -> DomainManager:
    try:
        return _MANAGER_CLASSES[name](store)
    except KeyError as exc:
        raise FactoryError(f"unknown manager {name}") from exc
