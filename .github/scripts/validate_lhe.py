"""Check the structure and event count of a Les Houches Event file."""

from xml.etree import ElementTree


def validate(path, expected):
    minimum, separator, maximum = str(expected).partition("-")
    minimum = int(minimum)
    maximum = int(maximum) if separator else minimum
    if not 0 < minimum <= maximum:
        raise ValueError("Expected a positive event count or an increasing range")

    with path.open("rb") as stream:
        elements = ElementTree.iterparse(stream, events=("start", "end"))
        _, root = next(elements)
        if root.tag != "LesHouchesEvents":
            raise ValueError("Expected a LesHouchesEvents document")

        depth = 1
        initialized = False
        count = 0
        for action, element in elements:
            if action == "start":
                depth += 1
                continue
            if depth == 2:
                if element.tag == "init":
                    initialized = bool(element.text and element.text.strip())
                elif element.tag == "event":
                    if not initialized:
                        raise ValueError("Missing LHE initialization before events")
                    count += 1
                    if not element.text or not element.text.strip():
                        raise ValueError(f"Empty LHE event {count}")
                root.remove(element)
            depth -= 1

    if not minimum <= count <= maximum:
        raise ValueError(f"Event count mismatch: got {count}, expected {expected}")
    return {"valid": True, "entries": count, "scope": "LHE structure and event count"}
