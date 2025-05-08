from .server import serve


def main():
    """MCP Windows Sound Server - Play Windows system sounds through MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to play Windows system sounds"
    )
    parser.add_argument("--sound-folder", type=str, help="Override default Windows sound folder")

    args = parser.parse_args()
    asyncio.run(serve(args.sound_folder))


if __name__ == "__main__":
    main()