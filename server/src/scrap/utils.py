# Contains functions only for data manipulation and restructuring
def is_image_format_valid(image_format):
    return image_format.lower() in ["image/jpg", "image/jpeg", "image/png"]


def filter_cse_images_results(results: list):
    filtered_results = []
    for result in results:
        if "mime" not in result:
            continue
        if is_image_format_valid(result["mime"]):
            filtered_results.append(result)

    return filtered_results
