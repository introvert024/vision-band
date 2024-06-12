from gradio_client import Client, handle_file

client = Client("krishnv/ImageCaptioning")
result = client.predict(
		image=handle_file('object____/test.jpeg'),
		api_name="/predict"
)
print(result)

# from gradio_client import Client

# client = Client("https://pragnakalp-ocr-image-to-text-zerogpu.hf.space/--replicas/7931m/")
# result = client.predict('PaddleOCR',
# 		'https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png',
# 		api_name="/predict"
# )
# print(result)