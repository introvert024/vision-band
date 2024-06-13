from gradio_client import Client, handle_file

client = Client("krishnv/OCR-image-to-text-ZeroGPU")
result = client.predict(
		Method="PaddleOCR",
		img=handle_file('read/download.png'),
		api_name="/predict"
)
print(result)