var roomNameElement = document.getElementById("room-name");
var roomName = roomNameElement ? JSON.parse(roomNameElement.textContent) : null;
// Define the <ul> element that contains the conversation list
let conversationList = document.querySelector("#contacts ul");
let searchInput = document.querySelector('input[name="search"]');
let previousConversationAPIUrl = `${window.location.protocol}//${window.location.host}/chat/conversations/`;
let conversationData;

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const hour = date.getHours();
  const minute = date.getMinutes();

  const formattedTime = `${hour < 10 ? "0" : ""}${hour}:${
    minute < 10 ? "0" : ""
  }${minute}`;
  return formattedTime;
};

const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();

  const formattedDate = `${year}-${month < 10 ? "0" : ""}${month}-${
    day < 10 ? "0" : ""
  }${day}`;
  return formattedDate;
};

const formatDateTime = (timestamp) => {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hour = date.getHours();
  const minute = date.getMinutes();

  const formattedDate = `${year}-${month < 10 ? "0" : ""}${month}-${
    day < 10 ? "0" : ""
  }${day}`;
  
  const formattedTime = `${hour < 10 ? "0" : ""}${hour}:${
    minute < 10 ? "0" : ""
  }${minute}`;
  return formattedDate + " " + formattedTime;
};

// Update the conversation list with the new data
const handleConversationListMessage = (conversation, prepend = false) => {
  var activeStatus = conversation.chat_user.online_status
    ? "online"
    : "offline";
  var unreadMessage = conversation.unread_counts
    ? `<div class="badge">${conversation.unread_counts}</div>`
    : "";
  var lastMessage = "";
  const li = document.createElement("li");
  li.setAttribute("id", `conversation-${conversation.chat_user.id}`);
  li.classList.add("contact");
  roomName === conversation.chat_user.agent_id
    ? li.classList.add("active")
    : null;
  if (conversation.last_message) {
    const messageSentTime = new Date(conversation.last_message.timestamp);
    const formattedTime = formatTime(messageSentTime);
    if (conversation.last_message.content_type === "text") {
      lastMessage = `
        <div class="text-end timer">
          <p class="mb-0">${formattedTime}</p>
        </div>
        <div class="message-bottom">
          <div class="preview">
            ${conversation.last_message.message}
            ${unreadMessage}
          </div>
        </div>
        `;
    } else {
      lastMessage = `
        <div class="text-end timer">
          <p class="mb-0">${formattedTime}</p>
        </div>
        <div class="message-bottom">
          <div class="preview">
            ${conversation.last_message.message_attachment.title}
            ${unreadMessage}
          </div>
        </div>
      `;
    }
  }
  li.innerHTML =
    `
        <a href="/chat/${conversation.chat_user.agent_id}" class="chatRoomLink">
        <div class="wrap position-relative">
          <span class="contact-status ${activeStatus}"></span>
          <img
            src="http://emilcarlsson.se/assets/harveyspecter.png"
            alt="${conversation.chat_user.full_name}"
          />
          <div class="meta">
            <p class="name position-relative">${conversation.chat_user.full_name}</p>
          ` +
    lastMessage +
    `
          </div>
        </div>
      </a>
  `;
  prepend ? conversationList.prepend(li) : conversationList.appendChild(li);
};

// Set up the WebSocket connection and message handling
const setupConversationListWebSocket = () => {
  conversationListSocket.onmessage = (event) => {
    var data = JSON.parse(event.data);
    handleConversationListMessage(data.conversation, (prepend = true));
    data = null;
  };
};

// Load the previous conversation
const loadPreviousConversation = async (url = null) => {
  url = url ? url : previousConversationAPIUrl;
  fetch(url)
    .then(async (resp) => {
      data = await resp.json();
      if (data.results.length > 0) {
        Object.values(data.results.reverse()).forEach((item, index, array) => {
          handleConversationListMessage(item);
        });
      } else {
        const li = document.createElement("li");
        li.innerHTML = `<strong>No record found!</strong>`;
        conversationList.appendChild(li);
      }
    })
    .catch((err) => console.error({ err }));
};
const updateActiveStatus = (data) => {
  const userStatus = document.querySelector("#user-active");
  var conversationListElement = document.querySelector(
    `#conversation-${data.user_id}`
  );
  if (conversationListElement) {
    conversationStatus =
      conversationListElement.querySelector(".contact-status");
    if (data.status) {
      userStatus ? userStatus.innerText = "Online" : null;
      conversationStatus.classList.add("online");
      conversationStatus.classList.remove("offline");
    } else {
      userStatus ? userStatus.innerText = "Offline" : null;
      conversationStatus.classList.add("online");
      conversationStatus.classList.remove("online");
    }
  }
};
async function messageReceivedNotification() {
  audio = new Audio(
    notificationToneFile
  );
  await audio.play();
}
const updateConversationList = async (data) => {
  messageReceivedNotification();
  var conversationListElement = document.querySelector(
    `#conversation-${data.content.chat_user.id}`
  );
  var conversationMeta = conversationListElement.querySelector(".meta");
  var unreadMessageCount = Number(
    conversationMeta.querySelector(".badge").innerText
  );
  var content = data.content;
  var unreadMessage = unreadMessageCount
    ? `<div class="badge">${++unreadMessageCount}</div>`
    : "";
  var formattedTime = formatTime(content.timestamp);
  if (roomName !== content.chat_user.agent_id) {
    messageReceivedNotification();
    conversationMeta.innerHTML = `
    <p class="name position-relative">${content.chat_user.agent_id}</p>
    <div class="text-end timer">
      <p class="mb-0">${formattedTime}</p>
    </div>
    <div class="message-bottom">
      <div class="preview">
        ${content.message}
        ${unreadMessage}
      </div>
    </div>
  `;
  }
};
