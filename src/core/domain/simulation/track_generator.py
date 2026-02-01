from typing import List
from src.core.domain.simulation.track_segment import TrackSegment


class TrackGenerator:
    @staticmethod
    def generate_track() -> List[TrackSegment]:
        return [
            TrackSegment(8.0, 290.0, 0.0, "STRAIGHT", 0.0),
            TrackSegment(2.0, 80.0, 290.0, "CORNER_ENTRY", 0.0),
            TrackSegment(1.5, 75.0, 80.0, "CORNER_MID", 0.8),
            TrackSegment(3.0, 200.0, 75.0, "CORNER_EXIT", 0.0),
            TrackSegment(2.0, 240.0, 200.0, "STRAIGHT", 0.0),
            TrackSegment(2.5, 120.0, 240.0, "CORNER_ENTRY", 0.0),
            TrackSegment(3.0, 110.0, 120.0, "CORNER_MID", -0.6),
            TrackSegment(2.5, 220.0, 110.0, "CORNER_EXIT", 0.0),
            TrackSegment(6.0, 310.0, 220.0, "STRAIGHT", 0.0),
        ]
