# Adapted from ianna/mcp-server-key4hep at bde7af183f57d14cabc809f1d35b281cd4d5dd69.
"""Read every event with podio's backend-independent reader.

This is structural validation, not a physics-reference comparison. Importing
edm4hep loads dictionaries required by podio. Run in the selected stack.
"""

import math
from pathlib import Path


def validate(path, expected):
    import edm4hep  # noqa: F401
    import ROOT
    from podio.reading import get_reader

    if expected <= 0 or not Path(path).is_file() or Path(path).stat().st_size == 0:
        raise ValueError("Expected a nonempty output and a positive event count")
    reader = get_reader(str(path))
    if "events" not in reader.categories:
        raise ValueError("No events category")
    frames = reader.get("events")
    if len(frames) != expected:
        raise ValueError(f"Event count mismatch: {len(frames)} != {expected}")
    particles_total = 0
    schema = None
    for frame in frames:
        names = set(frame.getAvailableCollections())
        if "MCParticles" not in names:
            raise ValueError("Missing MCParticles collection")
        if schema is None:
            schema = sorted(names)
        elif sorted(names) != schema:
            raise ValueError("Collection names change between events")
        # Force deserialization of every collection, not just the tree header.
        for name in names:
            collection = frame.get(name)
            for _ in collection:
                pass
        particles = frame.get("MCParticles")
        # podio returns std::string_view from getTypeName(). Depending on the
        # cppyy/ROOT version, str(view) may describe the proxy instead of its
        # contents. Check the dictionary-backed C++ class, not its string proxy.
        if not isinstance(particles, ROOT.edm4hep.MCParticleCollection):
            actual = getattr(type(particles), "__cpp_name__", type(particles).__name__)
            raise ValueError(
                "MCParticles has the wrong EDM4hep collection type: "
                f"expected edm4hep::MCParticleCollection, got {actual}"
            )
        identifiers = set()
        for particle in particles:
            oid = particle.getObjectID()
            identifiers.add((oid.collectionID, oid.index))
            momentum = particle.getMomentum()
            if not all(
                math.isfinite(v)
                for v in (
                    momentum.x,
                    momentum.y,
                    momentum.z,
                    particle.getMass(),
                    particle.getCharge(),
                )
            ):
                raise ValueError("Non-finite MCParticle values")
        for particle in particles:
            for related in [*particle.getParents(), *particle.getDaughters()]:
                if not related.isAvailable():
                    raise ValueError("Unresolved MCParticle relation")
                oid = related.getObjectID()
                if (oid.collectionID, oid.index) not in identifiers:
                    raise ValueError("MCParticle relation leaves the required collection")
        particles_total += len(particles)
    if particles_total == 0:
        raise ValueError("No MCParticles in generated sample")
    return {
        "valid": True,
        "entries": expected,
        "particles": particles_total,
        "collections": schema,
        "scope": "EDM4hep structure and MCParticle relations",
    }
