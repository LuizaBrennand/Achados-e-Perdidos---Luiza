// Pequenas melhorias de experiência: confirma ação e valida tamanho da imagem.
document.querySelectorAll("form[action^='/resolver/']").forEach(form => {
  form.addEventListener("submit", event => {
    if (!confirm("Deseja atualizar o status deste item?")) event.preventDefault();
  });
});
const upload = document.querySelector('input[type="file"]');
if (upload) upload.addEventListener("change", () => {
  const file = upload.files[0];
  if (file && file.size > 5 * 1024 * 1024) {
    alert("A imagem deve ter no máximo 5 MB.");
    upload.value = "";
  }
});