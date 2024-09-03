class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };

    this.state = false;
    this.messages = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener("click", () => this.toggleState(chatBox));
    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  toggleState(chatBox) {
    this.state = !this.state;

    // Hiển thị hoặc ẩn chatbox
    if (this.state) {
      chatBox.classList.add("chatbox--active");
    } else {
      chatBox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatBox) {
    var textField = chatBox.querySelector("input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }

    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);

    // Cập nhật giao diện chat với tin nhắn người dùng ngay lập tức
    this.updateChatText(chatBox);
    textField.value = "";

    // Gửi yêu cầu tới server để lấy phản hồi của bot
    fetch("http://127.0.0.1:5001/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { name: "Sam", message: r.answer };
        this.messages.push(msg2);
        this.updateChatText(chatBox);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  updateChatText(chatBox) {
    var html = "";
    this.messages.slice().forEach(function (item, index) {
      if (item.name === "Sam") {
        html +=
          '<div class="messages__item messages__item--visitor">' +
          item.message +
          "</div>";
      } else {
        html +=
          '<div class="messages__item messages__item--operator">' +
          item.message +
          "</div>";
      }
    });

    const chatMessage = chatBox.querySelector(".chatbox__messages div");
    chatMessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
