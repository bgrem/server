from uuid import uuid4

class ImageHelper:
    def __init__(
        self,
        user_id: str,
        input_image_url:str,
        output_image_url:str,
        image_id:str or None = None,
    ) -> None:
        self.user_id = user_id
        self.input_image_url = input_image_url
        self.output_image_url = output_image_url
        if not image_id:
            image_id = f"{uuid4()}"
        self.image_id = image_id
