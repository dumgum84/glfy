# glfy/cli.py

from .glfy_imports import *
from .config import DEFAULT_ASCII_CHARS, FONT_MAP
from .core import process_image, process_video, process_live_video
from .utils import (
    execute_ffmpeg_command,
    execute_ffmpeg_with_fallback,
    get_absolute_path
)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="glfy: Convert images and videos to ASCII art, or process live video streams.",
    )

    subparsers = parser.add_subparsers(dest='command', help='Available subcommands')

    # Image Processing Subcommand
    image_parser = subparsers.add_parser('image', help='Convert an image to ASCII art.')
    image_parser.add_argument("input_path", help="Path to the input image file.")
    image_parser.add_argument("-s", "--scale", type=float, default=1.0,
                              help="Scale factor for font size (default: 1.0).")
    image_parser.add_argument("-b", "--brightness", type=float, default=1.0, help="Brightness boost (default: 1.0)")
    image_parser.add_argument("-c", "--contrast", type=float, default=1.0, help="Contrast boost (default: 1.0)")
    image_parser.add_argument("-l", "--lightness", type=float, default=1.0, help="Lightness boost (default: 1.0)")
    image_parser.add_argument("-v", "--vibrancy", type=float, default=1.0, help="Vibrancy boost (default: 1.0)")
    image_parser.add_argument("-a", "--ascii_chars", type=str,
                              default=DEFAULT_ASCII_CHARS,
                              help="String of ASCII characters to use for conversion (dark to light).")
    image_parser.add_argument("-g", "--gamma", type=float, default=2.2, help="Gamma correction value (default: 2.2)")
    image_parser.add_argument("-hs", "--horizontal_spacing", type=int, default=10,
                              help="Horizontal spacing per ASCII character (default: 10)")
    image_parser.add_argument("-vs", "--vertical_spacing", type=int, default=20,
                              help="Vertical spacing per ASCII character (default: 20)")
    image_parser.add_argument("-bv", "--background_vibrancy", type=float, default=0.0,
                              help="Background vibrancy multiplier (default: 0.0).")
    image_parser.add_argument("-bb", "--background_brightness", type=float, default=0.0,
                              help="Background brightness multiplier (default: 0.0).")
    image_parser.add_argument("-bbr", "--background_blur_radius", type=int, default=100,
                              help="Background Gaussian blur radius (default: 100).")
    image_parser.add_argument("-r", "--resolution", type=str, default=None,
                              help="Target resolution for the output ASCII art in WIDTHxHEIGHT format, e.g., 1920x1080. If not specified, original resolution is used.")
    image_parser.add_argument("-bw", "--black_white", action="store_true", help="Render ASCII art in black and white.")
    image_parser.add_argument("-br", "--background_removal", action="store_true",
                              help="Enable background removal using MediaPipe Selfie Segmentation.")
    image_parser.add_argument("-t", "--typeface", type=str, default="dvsb",
                              help="Select the typeface to use. Options are 'dvs', 'dvsb', 'cn', 'cnb'. Default is 'dvsb'.")

    # Video Processing Subcommand
    video_parser = subparsers.add_parser('video', help='Convert a video to ASCII art.')
    video_parser.add_argument("input_path", help="Path to the input video file.")
    video_parser.add_argument("-s", "--scale", type=float, default=1.0,
                              help="Scale factor for font size (default: 1.0).")
    video_parser.add_argument("-f", "--fps", type=int, default=30, help="Frames per second for frame extraction (default: 30)")
    video_parser.add_argument("-b", "--brightness", type=float, default=1.0, help="Brightness boost (default: 1.0)")
    video_parser.add_argument("-c", "--contrast", type=float, default=1.0, help="Contrast boost (default: 1.0)")
    video_parser.add_argument("-l", "--lightness", type=float, default=1.0, help="Lightness boost (default: 1.0)")
    video_parser.add_argument("-v", "--vibrancy", type=float, default=1.0, help="Vibrancy boost (default: 1.0)")
    video_parser.add_argument("-a", "--ascii_chars", type=str,
                              default=DEFAULT_ASCII_CHARS,
                              help="String of ASCII characters to use for conversion (dark to light).")
    video_parser.add_argument("-g", "--gamma", type=float, default=2.2, help="Gamma correction value (default: 2.2)")
    video_parser.add_argument("-hs", "--horizontal_spacing", type=int, default=10,
                              help="Horizontal spacing per ASCII character (default: 10)")
    video_parser.add_argument("-vs", "--vertical_spacing", type=int, default=20,
                              help="Vertical spacing per ASCII character (default: 20)")
    video_parser.add_argument("-bv", "--background_vibrancy", type=float, default=0.0,
                              help="Background vibrancy multiplier (default: 0.0).")
    video_parser.add_argument("-bb", "--background_brightness", type=float, default=0.0,
                              help="Background brightness multiplier (default: 1.0).")
    video_parser.add_argument("-bbr", "--background_blur_radius", type=int, default=100,
                              help="Background Gaussian blur radius (default: 100).")
    video_parser.add_argument("-r", "--resolution", type=str, default=None,
                              help="Target resolution for the output ASCII art/video in WIDTHxHEIGHT format, e.g., 1920x1080. If not specified, original resolution is used.")
    video_parser.add_argument("-bw", "--black_white", action="store_true", help="Render ASCII art in black and white.")
    video_parser.add_argument("-br", "--background_removal", action="store_true",
                              help="Enable background removal using MediaPipe Selfie Segmentation.")
    video_parser.add_argument("-t", "--typeface", type=str, default="dvsb",
                              help="Select the typeface to use. Options are 'dvs', 'dvsb', 'cn', 'cnb'. Default is 'dvsb'.")

    # Live Video Processing Subcommand
    live_parser = subparsers.add_parser('live', help='Process live video and stream ASCII art to a virtual camera.')
    live_parser.add_argument("-s", "--scale", type=float, default=1.0,
                             help="Scale factor for font size (default: 1.0).")
    live_parser.add_argument("-f", "--fps", type=int, default=30, help="Frames per second for processing (default: 30)")
    live_parser.add_argument("-b", "--brightness", type=float, default=1.0, help="Brightness boost (default: 1.0)")
    live_parser.add_argument("-c", "--contrast", type=float, default=1.0, help="Contrast boost (default: 1.0)")
    live_parser.add_argument("-l", "--lightness", type=float, default=1.0, help="Lightness boost (default: 1.0)")
    live_parser.add_argument("-v", "--vibrancy", type=float, default=1.0, help="Vibrancy boost (default: 1.0)")
    live_parser.add_argument("-a", "--ascii_chars", type=str,
                             default=DEFAULT_ASCII_CHARS,
                             help="String of ASCII characters to use for conversion (dark to light).")
    live_parser.add_argument("-g", "--gamma", type=float, default=2.2, help="Gamma correction value (default: 2.2)")
    live_parser.add_argument("-hs", "--horizontal_spacing", type=int, default=10,
                             help="Horizontal spacing per ASCII character (default: 10)")
    live_parser.add_argument("-vs", "--vertical_spacing", type=int, default=20,
                             help="Vertical spacing per ASCII character (default: 20)")
    live_parser.add_argument("-bv", "--background_vibrancy", type=float, default=0.0,
                             help="Background vibrancy multiplier (default: 0.0).")
    live_parser.add_argument("-bb", "--background_brightness", type=float, default=0.0,
                             help="Background brightness multiplier (default: 0.0).")
    live_parser.add_argument("-bbr", "--background_blur_radius", type=int, default=100,
                             help="Background Gaussian blur radius (default: 100).")
    live_parser.add_argument("-r", "--resolution", type=str, default=None,
                             help="Target resolution for the output ASCII art/video in WIDTHxHEIGHT format, e.g., 1920x1080. If not specified, original resolution is used.")
    live_parser.add_argument("-bw", "--black_white", action="store_true", help="Render ASCII art in black and white.")
    live_parser.add_argument("-br", "--background_removal", action="store_true",
                             help="Enable background removal using MediaPipe Selfie Segmentation.")
    live_parser.add_argument("-t", "--typeface", type=str, default="dvsb",
                             help="Select the typeface to use. Options are 'dvs', 'dvsb', 'cn', 'cnb'. Default is 'dvsb'.")
    live_parser.add_argument("-src", "--source", type=str, choices=['cam', 'scr'], default='scr',
                             help="Source for live video: 'cam' (camera) or 'scr' (screen) (default: 'scr').")

    return parser.parse_args()

def main():
    args = parse_arguments()

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Ensure a subcommand is provided
    if not args.command:
        print("Error: No subcommand provided. Use -h for help.", file=sys.stderr)
        sys.exit(1)

    # Set up font path and size based on subcommand
    typeface = args.typeface.lower()
    if typeface not in FONT_MAP:
        logging.warning(f"Typeface '{typeface}' not recognized. Defaulting to 'dvsb'.")
        typeface = 'dvsb'

    # Get the absolute path to the font file using utils.py
    font_path = get_absolute_path(os.path.join("fonts", FONT_MAP[typeface]))

    if not os.path.exists(font_path):
        logging.error(f"Error: Font file not found at {font_path}.")
        sys.exit(1)

    try:
        font_size = max(1, int(12 * args.scale))  # Ensure font size is at least 1
        font = ImageFont.truetype(font_path, font_size)
        scaled_hs = max(1, int(args.horizontal_spacing * args.scale))
        scaled_vs = max(1, int(args.vertical_spacing * args.scale))
        logging.info(f"Loaded font '{typeface}' from {font_path} with size {font_size}.")
        logging.info(f"Scaled horizontal_spacing: {scaled_hs}, Scaled vertical_spacing: {scaled_vs}.")
    except Exception as e:
        logging.error(f"Error loading font: {e}")
        sys.exit(1)

    # Parse resolution if specified
    target_width, target_height = None, None
    if args.resolution:
        try:
            target_width, target_height = map(int, args.resolution.lower().split('x'))
            logging.info(f"Requested target resolution: {target_width}x{target_height}.")
        except ValueError:
            logging.error("Error: Resolution must be in the format WIDTHxHEIGHT.")
            sys.exit(1)

    # Initialize MediaPipe Selfie Segmentation if background removal is enabled
    selfie_segmentation = None
    if args.background_removal:
        try:
            import mediapipe as mp
            selfie_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)
        except ImportError:
            logging.error("Error: MediaPipe is not installed. Please install it using 'pip install mediapipe'.")
            sys.exit(1)

    # Dispatch to the appropriate processing function based on subcommand
    if args.command == 'image':
        process_image(
            input_path=args.input_path,
            scale_factor=args.scale,
            brightness_boost=args.brightness,
            contrast_boost=args.contrast,
            lightness_boost=args.lightness,
            vibrancy_boost=args.vibrancy,
            ascii_chars=args.ascii_chars,
            gamma=args.gamma,
            horizontal_spacing=scaled_hs,
            vertical_spacing=scaled_vs,
            background_vibrancy=args.background_vibrancy,
            background_brightness=args.background_brightness,
            background_blur_radius=args.background_blur_radius,
            target_width=target_width,
            target_height=target_height,
            font=font,
            black_and_white=args.black_white,
            background_removal=args.background_removal,
            selfie_segmentation=selfie_segmentation
        )
    elif args.command == 'video':
        process_video(
            input_path=args.input_path,
            scale_factor=args.scale,
            fps=args.fps,
            brightness_boost=args.brightness,
            contrast_boost=args.contrast,
            lightness_boost=args.lightness,
            vibrancy_boost=args.vibrancy,
            ascii_chars=args.ascii_chars,
            gamma=args.gamma,
            horizontal_spacing=scaled_hs,
            vertical_spacing=scaled_vs,
            background_vibrancy=args.background_vibrancy,
            background_brightness=args.background_brightness,
            background_blur_radius=args.background_blur_radius,
            target_width=target_width,
            target_height=target_height,
            font=font,
            black_and_white=args.black_white,
            background_removal=args.background_removal
        )
    elif args.command == 'live':
        process_live_video(
            scale_factor=args.scale,
            fps=args.fps,
            brightness_boost=args.brightness,
            contrast_boost=args.contrast,
            lightness_boost=args.lightness,
            vibrancy_boost=args.vibrancy,
            ascii_chars=args.ascii_chars,
            gamma=args.gamma,
            horizontal_spacing=scaled_hs,
            vertical_spacing=scaled_vs,
            background_vibrancy=args.background_vibrancy,
            background_brightness=args.background_brightness,
            background_blur_radius=args.background_blur_radius,
            font=font,
            target_width=target_width,
            target_height=target_height,
            black_and_white=args.black_white,
            background_removal=args.background_removal,
            source=args.source,
            selfie_segmentation=selfie_segmentation
        )
    else:
        logging.error("Error: Unknown command.")
        sys.exit(1)

    # Close the segmentation model if initialized
    if selfie_segmentation:
        selfie_segmentation.close()

if __name__ == "__main__":
    main()