from typing import List

from unstructured.documents.elements import Element
from unstructured.partition.pdf import partition_pdf as partition_pdf_original


def partition_pdf(**kwargs) -> List[Element]:
    elements: List[Element] = partition_pdf_original(
        extract_images_in_pdf=kwargs.pop('extract_images_in_pdf', True),
        extract_image_block_to_payload=kwargs.pop('extract_image_block_to_payload', True),
        extract_image_block_types=kwargs.pop('extract_image_block_types', ["Image"]),
        **kwargs,
    )

    pdf_elements: List[Element] = []

    for element in elements:

        # Bullet points are accidentally extracted by unstructured
        if len(element.text) == 1:
            continue

        pdf_elements.append(element)

    return pdf_elements


__all__ = ['partition_pdf']
