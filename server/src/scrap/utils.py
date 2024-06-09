# Contains functions only for data manipulation and restructuring
def is_image_format_valid(image_format):
    """
    Checks if the provided image format is valid.
    :param image_format: The image format to validate
    :return: True if the image format is valid, False otherwise
    """
    return image_format.lower() in ["image/jpg", "image/jpeg", "image/png"]


def filter_cse_images_results(results: list):
    """
    Filters the provided list of results to only include those with valid image formats.
    :param results: The list of results to filter
    :return: The filtered list of results containing only valid image formats
    """
    filtered_results = []
    for result in results:
        if "mime" not in result:
            continue
        if is_image_format_valid(result["mime"]):
            filtered_results.append(result)
    return filtered_results
