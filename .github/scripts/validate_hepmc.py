"""Check the framing and event count of a HepMC3 ASCII file."""

START = "HepMC::Asciiv3-START_EVENT_LISTING"
END = "HepMC::Asciiv3-END_EVENT_LISTING"


def validate(path, expected):
    if expected <= 0:
        raise ValueError("Expected a positive event count")

    count = 0
    with path.open() as stream:
        if not next(stream, "").startswith("HepMC::Version ") or next(stream, "").strip() != START:
            raise ValueError("Expected a HepMC3 ASCII header")

        declared_particles = particles = 0
        for line in stream:
            record = line.split()
            if not record:
                continue
            if record[0] in ("E", END):
                if particles != declared_particles:
                    raise ValueError(f"Particle count mismatch in HepMC event {count}")
                if record[0] == END:
                    break
                count += 1
                declared_particles = int(record[3])
                if declared_particles <= 0:
                    raise ValueError(f"Empty HepMC event {count}")
                particles = 0
            elif record[0] == "P":
                particles += 1
        else:
            raise ValueError("Missing HepMC3 end marker")
        if any(line.strip() for line in stream):
            raise ValueError("Unexpected data after the HepMC3 end marker")

    if count != expected:
        raise ValueError(f"Event count mismatch: {count} != {expected}")
    return {"valid": True, "entries": count, "scope": "HepMC3 ASCII framing and event count"}
