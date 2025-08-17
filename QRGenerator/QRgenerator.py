import qrcode
import threading
from PIL import Image


class QRGenerator:
    _instance = None  # Store the single instance of the class
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Override __new__ to ensure only one instance of QRGenerator."""
        with cls._lock:
            if not cls._instance:
                cls._instance = super(QRGenerator, cls).__new__(cls, *args, **kwargs)
                cls._instance._initialize()  # Initialize the instance only once
            return cls._instance

    def _initialize(self):
        """Initialize the QRCode object only once."""
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        print("Created QRGenerator\n------------")

    @classmethod
    def Instance(cls):
        """Return the Singleton instance."""
        return cls()

    def generate_qr(self, data: str, filename: str = None) -> Image:
        """
        Generates a QR code based on the provided data.
        Optionally saves the QR code to a file.

        Args:
            data (str): The data to encode in the QR code.
            filename (str, optional): If provided, the QR code will be saved to this file.

        Returns:
            Image: The generated QR code image.
        """
        # Clear any previous QR code data and add new data
        self.qr.clear()
        self.qr.add_data(data)
        self.qr.make(fit=True)

        # Create the image from the QR code
        img = self.qr.make_image(fill='black', back_color='white')

        # Save to file if a filename is provided
        if filename:
            img.save(filename + ".png")
            print(f"QR code saved as {filename}.png")

        # Return the generated image
        return img


# Example usage of QRGenerator Singleton
if __name__ == "__main__":
    qr_gen = QRGenerator.Instance()  # Access Singleton via Instance
    qr_gen.generate_qr("https://www.example.com", "example_qr")
    qr_gen.generate_qr("https://www.anotherexample.com")
