import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt

def train():
    import numpy as np  

    torch.manual_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    batch_size = 64
    latent_dim = 100
    image_size = 28 * 28
    num_epochs = 50

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    mnist_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    dataloader = DataLoader(mnist_dataset, batch_size=batch_size, shuffle=True, num_workers=2)

    class Generator(nn.Module):
        def __init__(self):
            super(Generator, self).__init__()
            self.model = nn.Sequential(
                nn.Linear(latent_dim, 256),
                nn.LeakyReLU(0.2),
                nn.BatchNorm1d(256),

                nn.Linear(256, 512),
                nn.LeakyReLU(0.2),
                nn.BatchNorm1d(512),

                nn.Linear(512, 1024),
                nn.LeakyReLU(0.2),
                nn.BatchNorm1d(1024),

                nn.Linear(1024, image_size),
                nn.Tanh()
            )

        def forward(self, z):
            img = self.model(z)
            return img.view(-1, 1, 28, 28)

    class Discriminator(nn.Module):
        def __init__(self):
            super(Discriminator, self).__init__()
            self.model = nn.Sequential(
                nn.Linear(image_size, 512),
                nn.LeakyReLU(0.2),

                nn.Linear(512, 256),
                nn.LeakyReLU(0.2),

                nn.Linear(256, 1),
                nn.Sigmoid()
            )

        def forward(self, img):
            img_flat = img.view(-1, image_size)
            validity = self.model(img_flat)
            return validity

    generator = Generator().to(device)
    discriminator = Discriminator().to(device)

    optimizer_G = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
    optimizer_D = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

    adversarial_loss = nn.BCELoss()

    g_losses = []
    d_losses = []
    real_accuracies = []
    fake_accuracies = []

    for epoch in range(num_epochs):
        epoch_g_loss = 0
        epoch_d_loss = 0
        epoch_real_acc = 0
        epoch_fake_acc = 0

        for i, (real_imgs, _) in enumerate(dataloader):
            current_batch_size = real_imgs.size(0)
            real_imgs = real_imgs.to(device)
            real_label = torch.ones(current_batch_size, 1).to(device)
            fake_label = torch.zeros(current_batch_size, 1).to(device)

            optimizer_G.zero_grad()

            z = torch.randn(current_batch_size, latent_dim).to(device)
            fake_imgs = generator(z)

            g_loss = adversarial_loss(discriminator(fake_imgs), real_label)
            g_loss.backward()
            optimizer_G.step()

            optimizer_D.zero_grad()

            real_preds = discriminator(real_imgs)
            fake_preds = discriminator(fake_imgs.detach())

            real_loss = adversarial_loss(real_preds, real_label)
            fake_loss = adversarial_loss(fake_preds, fake_label)
            d_loss = (real_loss + fake_loss) / 2

            d_loss.backward()
            optimizer_D.step()

            real_acc = ((real_preds > 0.5).float() == real_label).float().mean().item()
            fake_acc = ((fake_preds > 0.5).float() == fake_label).float().mean().item()

            epoch_g_loss += g_loss.item()
            epoch_d_loss += d_loss.item()
            epoch_real_acc += real_acc
            epoch_fake_acc += fake_acc

            if i % 100 == 0:
                print(f"[Epoch {epoch}/{num_epochs}] [Batch {i}/{len(dataloader)}] "
                      f"[D loss: {d_loss.item():.4f}] [G loss: {g_loss.item():.4f}] "
                      f"[Real acc: {real_acc:.4f}] [Fake acc: {fake_acc:.4f}]")

        epoch_g_loss /= len(dataloader)
        epoch_d_loss /= len(dataloader)
        epoch_real_acc /= len(dataloader)
        epoch_fake_acc /= len(dataloader)

        g_losses.append(epoch_g_loss)
        d_losses.append(epoch_d_loss)
        real_accuracies.append(epoch_real_acc)
        fake_accuracies.append(epoch_fake_acc)

        print(f"[Epoch {epoch}/{num_epochs}] "
              f"[D loss: {epoch_d_loss:.4f}] [G loss: {epoch_g_loss:.4f}] "
              f"[D real acc: {epoch_real_acc:.4f}] [D fake acc: {epoch_fake_acc:.4f}]")

        if epoch % 5 == 0:
            with torch.no_grad():
                sample_z = torch.randn(25, latent_dim).to(device)
                gen_imgs = generator(sample_z).cpu().detach()

                fig, axs = plt.subplots(5, 5, figsize=(10, 10))
                for ax_i, ax in enumerate(axs.flat):
                    ax.imshow(gen_imgs[ax_i, 0].numpy(), cmap='gray')
                    ax.axis('off')
                plt.savefig(f"gan_generated_epoch_{epoch}.png")
                plt.close()

    print("Training completed!")

    with torch.no_grad():
        sample_z = torch.randn(16, latent_dim).to(device)
        gen_imgs = generator(sample_z).cpu().detach()

        fig, axs = plt.subplots(4, 4, figsize=(8, 8))
        for ax_i, ax in enumerate(axs.flat):
            ax.imshow(gen_imgs[ax_i, 0].numpy(), cmap='gray')
            ax.axis('off')
        plt.savefig("final_gan_generated.png")
        plt.show()

    torch.save(generator.state_dict(), "gan_generator.pth")
    torch.save(discriminator.state_dict(), "gan_discriminator.pth")
