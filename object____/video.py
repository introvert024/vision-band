from gradio_client import Client

client = Client("https://damo-nlp-sg-video-llama.hf.space/")
result = client.predict(
				"https://github.com/gradio-app/gradio/raw/main/test/test_files/video_sample.mp4",	
				"",	
				"explain what you see",	
				"null",	
				fn_index=2
)
print(result)