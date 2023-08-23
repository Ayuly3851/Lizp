from application import create_app

__import__('os').system('cls')

app = create_app()

if __name__ == '__main__':
	app.run(debug = True)