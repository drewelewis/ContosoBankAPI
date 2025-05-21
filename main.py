if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            log_level="debug",
            reload=False,)
    except Exception as e:
        print("Unable to start the uvicorn server")
        print(e)





