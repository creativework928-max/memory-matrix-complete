export class ModalManager {
  constructor() {
    this.confirmHandler = null;

    document.addEventListener("click", (event) => {
      const closeButton = event.target.closest("[data-close-modal]");

      if (!closeButton) {
        return;
      }

      this.close(closeButton.dataset.closeModal);
    });
  }

  open(id) {
    const modal = document.getElementById(id);

    if (!modal) {
      return;
    }

    if (typeof modal.showModal === "function") {
      if (!modal.open) {
        modal.showModal();
      }
    } else {
      modal.setAttribute("open", "");
    }
  }

  close(id) {
    const modal = document.getElementById(id);

    if (!modal) {
      return;
    }

    if (typeof modal.close === "function") {
      modal.close();
    } else {
      modal.removeAttribute("open");
    }
  }

  closeAll() {
    document.querySelectorAll("dialog[open]").forEach((dialog) => {
      if (typeof dialog.close === "function") {
        dialog.close();
      } else {
        dialog.removeAttribute("open");
      }
    });
  }

  confirm({
    title,
    message,
    confirmText = "CONFIRM",
    onConfirm,
  }) {
    document.getElementById("confirm-title").textContent = title;
    document.getElementById("confirm-message").textContent = message;
    document.getElementById("confirm-yes").textContent = confirmText;

    this.confirmHandler = onConfirm;
    this.open("confirm-modal");
  }

  resolveConfirm() {
    const handler = this.confirmHandler;
    this.confirmHandler = null;
    this.close("confirm-modal");

    if (handler) {
      handler();
    }
  }

  cancelConfirm() {
    this.confirmHandler = null;
    this.close("confirm-modal");
  }
}
