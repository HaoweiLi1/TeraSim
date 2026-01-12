from pathlib import Path
import sys
import argparse

from terasim_cosmos import TeraSimToCosmosConverter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert TeraSim simulation data to Cosmos-Drive compatible format"
    )

    # Required parameters
    parser.add_argument("--path_to_output", type=Path, default=Path("/home/haowei/Documents/TeraSim/CrashCase_HD_Video/crash_2023197392/hdvideo"),
                        help="Output directory path")
    parser.add_argument("--path_to_fcd", type=Path, default=Path("/home/haowei/Documents/TeraSim/CrashCase_HD_Video/crash_2023197392/final.fcd.xml"),
                        help="Path to FCD (Floating Car Data) XML file")
    parser.add_argument("--path_to_map", type=Path, default=Path("/home/haowei/Documents/TeraSim/CrashCase_HD_Video/crash_2023197392/map.net.xml"),
                        help="Path to SUMO network map XML file")
    parser.add_argument("--time_start", type=float, default=1.1,
                        help="Start time in seconds")
    parser.add_argument("--time_end", type=float, default=5.0,
                        help="End time in seconds")
    parser.add_argument("--vehicle_id", type=str, default="vehicle0",
                        help="ID of the ego vehicle")

    # Optional parameters
    parser.add_argument("--camera_setting_name", type=str, choices=["default", "waymo"],
                        default="default",
                        help="Camera configuration setting (default: %(default)s)")
    parser.add_argument("--agent_clip_distance", type=float, default=160.0,
                        help="Distance threshold to show agents (default: %(default)s) meters")
    parser.add_argument("--map_clip_distance", type=float, default=200.0,
                        help="Distance threshold to show map features (default: %(default)s) meters")
    parser.add_argument("--google_model", type=str,
                        help="Google Gemini model name for street view description (e.g., gemini-2.5-pro)")
    parser.add_argument("--openrouter_model", type=str,
                        help="OpenRouter model name for street view description (e.g., google/gemini-2.5-pro)")

    # Processing options
    parser.add_argument("--streetview_retrieval", action="store_true",
                        help="Retrieve street view imagery and generate text descriptions")
    parser.add_argument("--no_streetview_retrieval", dest="streetview_retrieval", action="store_false",
                        help="Disable street view retrieval")
    parser.set_defaults(streetview_retrieval=True)

    args = parser.parse_args()

    # Create config dictionary from command line arguments
    config_dict = {
        "path_to_output": str(args.path_to_output),
        "path_to_fcd": str(args.path_to_fcd),
        "path_to_map": str(args.path_to_map),
        "camera_setting_name": args.camera_setting_name,
        "vehicle_id": args.vehicle_id,
        "time_start": args.time_start,
        "time_end": args.time_end,
        "agent_clip_distance": args.agent_clip_distance,
        "map_clip_distance": args.map_clip_distance,
        "streetview_retrieval": args.streetview_retrieval,
        "google_model": args.google_model,
        "openrouter_model": args.openrouter_model,
    }

    # Create converter and run conversion
    converter = TeraSimToCosmosConverter.from_config_dict(config_dict)
    converter.convert()