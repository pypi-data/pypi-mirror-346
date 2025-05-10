import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import torch
import torch.nn as nn
import torch.optim as optim

def run_all():
    device = torch.device("cpu")
    print("Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    print("Displaying sample images...")
    fig, axes = plt.subplots(2, 5, figsize=(10, 5))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(x_train[i], cmap='gray')
        ax.axis('off')
    plt.tight_layout()
    plt.show()

    print("Normalizing and flattening data...")
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    X_train = x_train.reshape(x_train.shape[0], -1)
    X_test = x_test.reshape(x_test.shape[0], -1)
    y_train = y_train.flatten()
    y_test = y_test.flatten()

    print("Training SVM classifier...")
    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train, y_train)
    y_pred = svm_model.predict(X_test)
    print("SVM Accuracy:", accuracy_score(y_test, y_pred))

    print("Building Neural Network model...")
    class NeuralNetwork(nn.Module):
        def __init__(self, input_size, num_classes):
            super(NeuralNetwork, self).__init__()
            self.fc1 = nn.Linear(input_size, 64)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(64, 32)
            self.fc3 = nn.Linear(32, num_classes)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x):
            x = self.relu(self.fc1(x))
            x = self.relu(self.fc2(x))
            x = self.softmax(self.fc3(x))
            return x

    model = NeuralNetwork(X_train.shape[1], 10)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Converting data to PyTorch tensors...")
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    print("Training Neural Network...")
    epochs = 5
    loss_values = []
    accuracy_values = []

    for epoch in range(epochs):
        model.train()
        outputs = model(X_train_tensor)
        loss = criterion(outputs, y_train_tensor)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        _, predicted_train = torch.max(outputs, 1)
        acc = (predicted_train == y_train_tensor).sum().item() / len(y_train_tensor)

        loss_values.append(loss.item())
        accuracy_values.append(acc)

        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}, Accuracy: {acc:.4f}")

    print("Plotting Loss and Accuracy graphs...")
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs + 1), loss_values, marker='o', label='Loss')
    plt.title("Loss vs Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs + 1), accuracy_values, marker='o', color='green', label='Accuracy')
    plt.title("Accuracy vs Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    print("Evaluating Neural Network...")
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        _, predicted = torch.max(test_outputs, 1)
        accuracy = (predicted == y_test_tensor).sum().item() / len(y_test_tensor)
        print("Neural Network Test Accuracy:", accuracy)

    print("Displaying predictions...")
    fig, axes = plt.subplots(2, 5, figsize=(10, 5))
    for i, ax in enumerate(axes.flatten()):
        ax.imshow(x_test[i], cmap='gray')
        ax.set_title(f"Pred: {predicted[i].item()}")
        ax.axis('off')
    plt.tight_layout()
    plt.show()

# Run everything
run_all()
