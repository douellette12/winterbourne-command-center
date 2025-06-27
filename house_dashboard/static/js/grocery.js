function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      // Does this cookie string begin with the name we want?
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('grocery-add-form');
  const itemList = document.getElementById('active-items'); // your UL element

  form?.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(form.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
      body: formData,
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          const li = document.createElement('li');
          li.className = 'list-group-item';
          li.innerHTML = `
            <div class="form-check">
              <input type="checkbox" class="form-check-input toggle-complete me-2" data-item-id="${data.id}">
              <label class="form-check-label">${data.title}</label>
            </div>
          `;
          itemList.appendChild(li);
          form.reset();
          const modal = bootstrap.Modal.getInstance(document.getElementById('groceryModal'));
          modal.hide();
        } else {
          alert(data.error || 'Error adding item');
        }
      });
  });
});



document.addEventListener('DOMContentLoaded', function () {
  document.body.addEventListener('click', function (e) {
    if (e.target.classList.contains('toggle-complete')) {
      const checkbox = e.target;
      const itemId = checkbox.dataset.itemId;

      fetch('/mealplan/grocery-list/toggle/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ id: itemId })
      })
      .then(response => response.json())
      .then(data => {
        const oldItem = document.getElementById(`item-${data.id}`);
        if (oldItem) oldItem.remove();

        const targetList = data.completed
          ? document.querySelector('#completed-items')
          : document.querySelector('#active-items');

        if (targetList) {
          targetList.insertAdjacentHTML('beforeend', data.html);
        }
        const inserted = document.querySelector(`#item-${data.id} input[type="checkbox"]`);
        if (inserted) {
          inserted.checked = data.completed;
        }
      })
      .catch(err => console.error(err));
    }
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const deleteModal = document.getElementById("deleteModal");
  const form = document.getElementById("delete-form");
  const itemNamePlaceholder = document.getElementById("item-name-placeholder");

  deleteModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;
    const itemId = button.getAttribute("data-item-id");
    const itemName = button.getAttribute("data-item-name");

    // Update modal display
    itemNamePlaceholder.textContent = itemName;

    // Set form action
    form.action = `/mealplan/grocery-list/delete/${itemId}/`;
  });

  // Intercept form submission to do AJAX
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const action = form.action;

    fetch(action, {
      method: "POST",
      headers: {
        "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
      },
    })
      .then(response => {
        if (response.redirected) {
          // Success: remove row, hide modal
          const id = action.split("/").filter(Boolean).pop();
          document.getElementById(`item-${id}`).remove();
          bootstrap.Modal.getInstance(deleteModal).hide();
        } else {
          console.error("Delete failed.");
        }
      });
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const editModal = document.getElementById("editModal");
  const editForm = document.getElementById("edit-form");
  const editNameInput = document.getElementById("edit-title");

  let currentEditId = null;

  editModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;
    currentEditId = button.getAttribute("data-item-id");
    const currentName = button.getAttribute("data-item-name");

    editNameInput.value = currentName;
    editForm.action = `/mealplan/grocery-list/edit/${currentEditId}/`;
  });

  editForm.addEventListener("submit", function (e) {
    e.preventDefault();

    fetch(editForm.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": editForm.querySelector("[name=csrfmiddlewaretoken]").value,
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({
        title: editNameInput.value
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.title) {
          // Update the name in the row
          const row = document.getElementById(`item-${data.id}`);
          row.querySelector(".form-check-label").innerText = data.title;

          const editButton = document.querySelector(`button[data-item-id="${data.id}"]`);
          if (editButton) {
            editButton.setAttribute('data-item-name', data.title);
          }

          // Hide modal
          bootstrap.Modal.getInstance(editModal).hide();
        }
      })
      .catch(err => {
        console.error("Edit failed", err);
      });
  });
});


function showCompletedSection() {
  var x = document.getElementById("completed-section");
  var btn = document.getElementById("show-completed-btn")
  if (x.style.display === "none") {
    x.style.display = "block";
    btn.innerHTML = "Hide Completed Items";
  } else {
    x.style.display = "none";
    btn.innerHTML = "Show Completed Items";
  }
}
