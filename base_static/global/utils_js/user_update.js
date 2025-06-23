document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("id_picture");
  const previewImage = document.getElementById("profilePreview");

  if (fileInput && previewImage) {
    fileInput.addEventListener("change", function (event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
          previewImage.src = e.target.result;
        };

        reader.readAsDataURL(file);
      }
    });
  }

  const editBtn = document.getElementById('editProfileBtn');
  const cancelBtn = document.getElementById('cancelEditBtn');
  const saveBtn = document.getElementById('saveProfileBtn');
  const form = document.querySelector('form');

  function setFormDisabled(disabled) {
    const fields = form.querySelectorAll('input, select, textarea');
    fields.forEach(field => {
      field.disabled = disabled;
    });
    // O botão salvar só está habilitado se o form não estiver bloqueado
    saveBtn.disabled = disabled;
  }

  // Começa com os campos e botão salvar desabilitados
  setFormDisabled(true);

  if (editBtn) {
    editBtn.addEventListener('click', function(e) {
      e.preventDefault();
      setFormDisabled(false);

      // Foca no primeiro campo
      const fields = form.querySelectorAll('input, select, textarea');
      if (fields.length > 0) fields[0].focus();
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener('click', function(e) {
      e.preventDefault();
      setFormDisabled(true);
    });
  }
});