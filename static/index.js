var formPost = document.querySelector("form");
var message = document.querySelector("#message");
var newPost = document.querySelector("#new-post");
var msgTimeout;

function msg(m) {
  message.hidden = false;
  message.textContent = m;
  if (msgTimeout) clearTimeout(msgTimeout);
  msgTimeout = setTimeout(() => {
    msgTimeout = null;
    message.hidden = true;
  }, 2000);
}

function addPost(post) {

}
function like() {
  msg("like");
}

function dislike() {
  msg("dislike");

}

function resposta() {

}

function novaPostagem() {
  formPost.hidden = false;
  newPost.hidden = true;
}

function fecharPostagem() {
  formPost.hidden = true;
  newPost.hidden = false;
}

function postar() {
  fecharPostagem();
  msg("Publicando...");
  fetch("/").then(res => res.text()).then(res => {
    msg("Publicado.");
    addPost(res);
  });
}

fetch("/posts").then(res => res.json()).then(res => {
  console.log(res);
});