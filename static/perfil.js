var form = document.querySelector("form");
var usuario = document.querySelector("input[name='usuario']");
var biografia = document.querySelector("input[name='biografia']");
var senha = document.querySelector("input[name='senha']");

function editar() {
  form.hidden = false;
}

function fechar() {
  form.hidden = true;
}