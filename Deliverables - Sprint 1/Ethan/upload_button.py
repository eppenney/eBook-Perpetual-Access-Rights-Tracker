
def uploadFile(self):
    # Gonna be honest, this section? ChatGPT
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)", options=options)

    if file_path:
        self.processFile(file_path)

def processFile(self, file_path):
    # Get that file
    file = pd.read_csv(file_path)
    # Print that file
    print(file.head())
    # Save to specific local file folder
    saveFolder = os.path.join(os.path.dirname(__file__), 'local_files')
    os.makedirs(saveFolder, exist_ok=True)
    savePath = os.path.join(saveFolder, 'processed_data.csv')
    file.to_csv(savePath, index=False)
    print(f"Saved to: {savePath}")