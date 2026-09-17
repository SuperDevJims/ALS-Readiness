from app.storage import build_key, upload_file

FOLDER_NAME = "test-assets"
BASE_PATH = "C:/Users/Gab/OneDrive/Documents/alsense_test_assets"

en_assets = [
    {
        "filename": "en-01",
        "ext": "png",
    },
    {
        "filename": "en-02",
        "ext": "png",
    },
    {
        "filename": "en-03",
        "ext": "png",
    },
    {
        "filename": "en-04",
        "ext": "png",
    },
    {
        "filename": "en-05",
        "ext": "png",
    },
    {
        "filename": "en-06",
        "ext": "jpg",
    },
    {
        "filename": "en-07",
        "ext": "jpg",
    },
    {
        "filename": "en-08",
        "ext": "jpg",
    },
    {
        "filename": "en-09",
        "ext": "png",
    },
    {
        "filename": "en-10",
        "ext": "png",
    },
    {
        "filename": "en-11",
        "ext": "png",
    },
]

fil_assets = [
    {
        "filename": "fil-01",
        "ext": "png",
    },
    {
        "filename": "fil-02",
        "ext": "png",
    },
    {
        "filename": "fil-03",
        "ext": "png",
    },
    {
        "filename": "fil-04",
        "ext": "png",
    },
    {
        "filename": "fil-05",
        "ext": "png",
    },
    {
        "filename": "fil-06",
        "ext": "png",
    },
    {
        "filename": "fil-07",
        "ext": "png",
    },
    {
        "filename": "fil-08",
        "ext": "png",
    },
    {
        "filename": "fil-09",
        "ext": "png",
    },
]

math_assets = [
    {
        "filename": "math-01",
        "ext": "png",
    },
    {
        "filename": "math-02",
        "ext": "png",
    },
    {
        "filename": "math-03",
        "ext": "png",
    },
    {
        "filename": "math-04",
        "ext": "png",
    },
    {
        "filename": "math-05",
        "ext": "png",
    },
]

assets = [*en_assets, *fil_assets, *math_assets]


def seed_bucket_test_assets():
    for asset in assets:

        filename = asset.get("filename")
        ext = asset.get("ext")

        key = build_key(
            FOLDER_NAME,
            f"{filename}.{ext}",
        )

        upload_file(
            f"{BASE_PATH}/{filename}.{ext}",
            key,
            f"image/{ext if ext != 'jpg' else 'jpeg'}",
        )

        print(f"{filename} - {key}")


if __name__ == "__main__":
    seed_bucket_test_assets()
