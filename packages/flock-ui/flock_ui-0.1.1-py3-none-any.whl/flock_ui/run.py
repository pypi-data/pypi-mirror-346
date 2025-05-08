import uvicorn

def main():
    uvicorn.run("flock_ui.app.main:app", host="127.0.0.1", port=8008, reload=True)

if __name__ == "__main__":
    main()

