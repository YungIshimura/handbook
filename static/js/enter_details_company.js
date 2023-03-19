// Общая функция сокрытия полей
function toggleFields(className, arrowClassName) {
    // Ищем все элементы с классом className.
    let toggleFields = document.querySelectorAll('.' + className);

    // Для каждого элемента с классом className
    toggleFields.forEach(function (toggleField) {
        // Ищем следующий элемент селектором '.hidden-field'.
        let hiddenFields = toggleField.nextElementSibling.querySelectorAll('.hidden-field');
        // Ищем элемент стрелки, который мы хотим поменять при переключении.
        let arrow = toggleField.querySelector(`.${arrowClassName}`);

        // Добавляем обработчик клика на элемент с классом className.
        toggleField.addEventListener("click", function () {
            // Для каждого блока с классом hidden-field в следующем элементе после toggleField
            hiddenFields.forEach(function (field) {
                // Если блок уже виден, скрываем его и меняем стрелку.
                if (field.style.display === "block") {
                    field.style.display = "none";
                    arrow.innerHTML = "&#9660;";
                } else {
                    // Иначе показываем блок и меняем стрелку.
                    field.style.display = "block";
                    arrow.innerHTML = "&#9650;";
                }
            });
        });
    });
}

toggleFields("toggle-fields-employee", "arrow-employee");
toggleFields("toggle-fields-branches", "arrow-branches");
toggleFields("toggle-fields-license", "arrow-license");
toggleFields("toggle-fields-site", "arrow-site");
toggleFields("toggle-fields-contact_phone", "arrow-contact_phone");
toggleFields("toggle-fields-contact_email", "arrow-contact_email");
toggleFields("toggle-fields-contact_url", "arrow-contact_url");


// Функция для получения значения cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Общая функция удаления объектов через модальное окно
function deleteItem(confirmModalId, confirmButtonId) {
    $(document).ready(function () {
        $(confirmModalId).on('show.bs.modal', function (e) {
            let itemPk = $(e.relatedTarget).data('item-Pk');
            let deleteUrl = $(e.relatedTarget).data('delete-url');
            $(confirmButtonId).data('item-Pk', itemPk);
            $(confirmButtonId).data('delete-url', deleteUrl);
        });

        $(confirmButtonId).click(function () {
            let itemPk = $(this).data('item-Pk');
            let deleteUrl = $(this).data('delete-url');
            let csrftoken = getCookie('csrftoken');
            $.ajax({
                type: 'POST',
                url: deleteUrl,
                data: {
                    csrfmiddlewaretoken: csrftoken,
                },
                success: function (data) {
                    if (data.success) {
                        $(confirmModalId).modal('hide');
                        location.reload();
                    } else if (data.error) {
                        $('.modal-body').html('Ошибка: ' + data.error);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    $('.modal-body').html('Ошибка: ' + textStatus);
                }
            });
        });
    });
}

$(document).ready(function () {
    deleteItem('#confirm-delete-employee-modal', '#confirm-delete-employee-btn');
    deleteItem('#confirm-delete-branches-modal', '#confirm-delete-branches-btn');
    deleteItem('#confirm-delete-license-modal', '#confirm-delete-license-btn');
    deleteItem('#confirm-delete-contact_phone-modal', '#confirm-delete-contact_phone-btn');
    deleteItem('#confirm-delete-contact_email-modal', '#confirm-delete-contact_email-btn');
    deleteItem('#confirm-delete-contact_url-modal', '#confirm-delete-contact_url-btn');
});


// Общая функция добавления объектов через модальное окно
$(document).ready(function () {
    const addEmployeeForm = $('#add-employee-modal-form');
    const addEmployeeModal = $('#add-employee-modal');

    const addBranchesForm = $('#add-branches-modal-form');
    const addBranchesModal = $('#add-branches-modal');

    const addLicenseForm = $('#add-license-modal-form');
    const addLicenseModal = $('#add-license-modal');

    const addContactPhoneForm = $('#add-contact_phone-modal-form');
    const addContactPhoneModal = $('#add-contact_phone-modal');

    const addContactEmailForm = $('#add-contact_email-modal-form');
    const addContactEmailModal = $('#add-contact_email-modal');

    const addContactUrlForm = $('#add-contact_url-modal-form');
    const addContactUrlModal = $('#add-contact_url-modal');

    // Общая функция для отправки данных формы на сервер через AJAX-запрос
    function sendData(form, url, successCallback, errorCallback) {
        $.ajax({
            url: url,
            method: 'POST',
            data: form.serialize(),
            success: successCallback,
            error: errorCallback
        });
    }

    // Обработчик ошибок при отправке данных на сервер
    function handleErrors(xhr, form) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#" + form.attr("id").replace("-modal-form", "") + "-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert(`Произошла ошибка при добавлении ${form.data("title")}`);
        }
    }

    // Обработчик успешной отправки данных на сервер
    function handleSuccess(form, modal) {
        // Закрываем модальное окно, очищаем форму и обновляем страницу
        modal.modal('hide');
        form[0].reset();
        location.reload();
    }

    // Очищаем сообщения об ошибках при каждом новом открытии формы
    addEmployeeModal.on('hidden.bs.modal', function () {
        addEmployeeForm.find(".error-message").text("").hide();
    });

    addBranchesModal.on('hidden.bs.modal', function () {
        addBranchesForm.find(".error-message").text("").hide();
    });

    addLicenseModal.on('hidden.bs.modal', function () {
        addLicenseForm.find(".error-message").text("").hide();
    });

    addContactPhoneModal.on('hidden.bs.modal', function () {
        addContactPhoneForm.find(".error-message").text("").hide();
    });

    addContactEmailModal.on('hidden.bs.modal', function () {
        addContactEmailForm.find(".error-message").text("").hide();
    });

    addContactUrlModal.on('hidden.bs.modal', function () {
        addContactUrlForm.find(".error-message").text("").hide();
    });

    // Отправляем данные формы на сервер при отправке формы
    addEmployeeForm.submit(function (event) {
        event.preventDefault();
        addEmployeeForm.find(".error-message").hide();
        sendData(addEmployeeForm, `/users/company/edit/${company_pk}/add_employee/`, function (data) {
            handleSuccess(addEmployeeForm, addEmployeeModal);
        }, function (xhr) {
            handleErrors(xhr, addEmployeeForm);
        });
    });

    addBranchesForm.submit(function (event) {
        event.preventDefault();
        addBranchesForm.find(".error-message").hide();
        sendData(addBranchesForm, `/users/company/edit/${company_pk}/add_branch/`, function (data) {
            handleSuccess(addBranchesForm, addBranchesModal);
        }, function (xhr) {
            handleErrors(xhr, addBranchesForm);
        });
    });

    addLicenseForm.submit(function (event) {
        event.preventDefault();
        addLicenseForm.find(".error-message").hide();
        sendData(addLicenseForm, `/users/company/edit/${company_pk}/add_license/`, function (data) {
            handleSuccess(addLicenseForm, addLicenseModal);
        }, function (xhr) {
            handleErrors(xhr, addLicenseForm);
        });
    });

    addContactPhoneForm.submit(function (event) {
        event.preventDefault();
        addContactPhoneForm.find(".error-message").hide();
        sendData(addContactPhoneForm, `/users/company/edit/${company_pk}/add_contact_phone/`, function (data) {
            handleSuccess(addContactPhoneForm, addContactPhoneModal);
        }, function (xhr) {
            handleErrors(xhr, addContactPhoneForm);
        });
    });

    addContactEmailForm.submit(function (event) {
        event.preventDefault();
        addContactEmailForm.find(".error-message").hide();
        sendData(addContactEmailForm, `/users/company/edit/${company_pk}/add_contact_email/`, function (data) {
            handleSuccess(addContactEmailForm, addContactEmailModal);
        }, function (xhr) {
            handleErrors(xhr, addContactEmailForm);
        });
    });

    addContactUrlForm.submit(function (event) {
        event.preventDefault();
        addContactUrlForm.find(".error-message").hide();
        sendData(addContactUrlForm, `/users/company/edit/${company_pk}/add_contact_url/`, function (data) {
            handleSuccess(addContactUrlForm, addContactUrlModal);
        }, function (xhr) {
            handleErrors(xhr, addContactUrlForm);
        });
    });

});


// Общая функция редактирования данных
function editData(data_type, pk_name, url, modal_id, form_id, handleSuccess, handleErrors) {
    $(document).on('click', `.edit-${data_type}-btn`, function () {
        let pk = $(this).data(`${pk_name}`);
        let update_url = $(this).data('update-url');
        let modal = $(`#${modal_id}`);

        $.ajax({
            url: `${url}/${pk}/`,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log(data);
                // Обновляем значения полей формы данными полученными из сервера
                for (const [key, value] of Object.entries(data)) {
                    modal.find(`#${key}`).val(value);
                }
                modal.find('form').attr('action', update_url);
            }
        });

        modal.find('form').off('submit').on('submit', function (e) {
            e.preventDefault();
            let form = $(this);

            // Очищаем сообщения об ошибках при каждом новом открытии формы
            modal.on('hidden.bs.modal', function () {
                $(".error-message").text("").hide();
            });

            // Функция, которая отправляет данные формы на сервер через AJAX-запрос
            function updateData() {
                $.ajax({
                    url: update_url,
                    type: 'POST',
                    data: form.serialize(),
                    dataType: 'json',
                    success: handleSuccess,
                    error: handleErrors
                });
            }

            // Отправляем данные формы на сервер при отправке формы
            $(".error-message").text("").hide();
            updateData();
        });
    });
}

// Редактирование сотрудника
editData('employee', 'employee-pk', '/users/get_employee_data', 'edit-employee-modal', 'edit-employee',
    function handleSuccess(data) {
        $('#edit-employee-modal').modal('hide');
        location.reload();
    },
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#edit-employee-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при обновлении данных сотрудника');
        }
    });


// Редактирование филиала
editData('branches', 'branche-pk', '/users/get_branche_data', 'edit-branches-modal', 'edit-branches',
    function handleSuccess(data) {
        $('#edit-branches-modal').modal('hide');
        location.reload();
    },
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#edit-branches-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при обновлении данных филиала');
        }
    });


// Редактирование лицензии
editData('license', 'license-pk', '/users/get_license_data', 'edit-license-modal', 'edit-license',
    function handleSuccess(data) {
        $('#edit-license-modal').modal('hide');
        location.reload();
    },
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#edit-license-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при обновлении данных лицензии');
        }
    });

// Редактирование телефонных номеров компании
editData('contact_phone', 'contact_phone-pk', '/users/get_contact_phone_data', 'edit-contact_phone-modal', 'edit-contact_phone',
    function handleSuccess(data) {
        $('#edit-contact_phone-modal').modal('hide');
        location.reload();
    },
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#edit-contact_phone-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при обновлении данных лицензии');
        }
    });

// Редактирование email компании
editData('contact_email', 'contact_email-pk', '/users/get_contact_email_data', 'edit-contact_email-modal', 'edit-contact_email',
    function handleSuccess(data) {
        $('#edit-contact_email-modal').modal('hide');
        location.reload();
    },
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#edit-contact_email-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при обновлении данных лицензии');
        }
    });

// Редактирование email компании
editData('contact_email', 'contact_email-pk', '/users/get_contact_email_data', 'edit-contact_email-modal', 'edit-contact_email',
    function handleSuccess(data) {
        $('#edit-contact_email-modal').modal('hide');
        location.reload();
    },
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#edit-contact_email-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при обновлении данных лицензии');
        }
    });


// Редактирование сайт компании
editData('contact_url', 'contact_url-pk', '/users/get_contact_url_data', 'edit-contact_url-modal', 'edit-contact_url',
    function handleSuccess(data) {
        $('#edit-contact_url-modal').modal('hide');
        location.reload();
    },
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#edit-contact_url-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при обновлении данных лицензии');
        }
    });


/* Блок выбора типов работ, выполняемых организацией и региона выполняемых*/

// функция обрабатывает удаление элемента span из его контейнера
function handleRemoveButtonClick(button, container, updateList) {
    // Получаем родительский элемент
    const span = button.parentNode;
    // Удаляем элемент <span>
    container.removeChild(span);
    // обновляем список после удаления элементов
    updateList();
}

// функция создает новый элемент span с заданным значением и добавляет к нему кнопку удаления
function createNewElement(value, container, listId, removeButtonClass, updateList) {
    // создаем новый элемент span и устанавливаем ему значение
    const newSpan = document.createElement('span');
    newSpan.textContent = value;
    // создаем кнопку удаления и добавляем класс
    const removeButton = document.createElement('span');
    removeButton.classList.add(removeButtonClass);
    removeButton.textContent = '✕';
    // добавляем кнопку удаления внутрь элемента span, а сам span в контейнер
    newSpan.appendChild(removeButton);
    container.appendChild(newSpan);
    // добавляем обработчик событий на кнопку удаления
    removeButton.addEventListener('click', () => {
        handleRemoveButtonClick(removeButton, container, updateList);
    });
    // обновляем список после удаления элементов
    updateList();
}

// функция обновляет список, заменяя старые элементы на новые
function updateList(containerId, listId) {
    // получаем контейнер и содержащийся в нем список
    const container = document.querySelector(`#${containerId}`);
    const list = document.querySelector(`#${listId}`);
    if (!container || !list) {
        return;
    }
    // очищаем список
    list.innerHTML = '';
    // для каждого элемента span в контейнере
    container.querySelectorAll('span').forEach(span => {
        // получаем значение
        const value = span.textContent;
        // создаем новый элемент li
        const li = document.createElement('li');
        // устанавливаем значение для li
        li.textContent = value;
        // добавим в список
        list.appendChild(li);
    });
}

// функция инициализирует кнопки удаления элементов
function initRemoveButtons(buttons, containerId, updateList) {
    // для каждой кнопки Х добавляем обработчик событий
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const container = document.querySelector(`#${containerId}`);
            handleRemoveButtonClick(button, container, updateList);
        });
    });
}

// функция инициализирует элемент select и обрабатывает его изменение
function initSelect(selectId, containerId, listId, removeButtonClass, updateList) {
    // получаем элемент select и контейнер
    const select = document.querySelector(`#${selectId}`);
    const container = document.querySelector(`#${containerId}`);

    // добавляем обработчик событий для изменения элемента select
    select.addEventListener('change', () => {
        // получаем выбранное значение
        const selectedValue = select.value;
        const elements = container.querySelectorAll('span');
        // устанавливаем флаг
        let valueExists = false;
        elements.forEach(span => {
            // если значение элемента повторяется
            if (span.textContent.includes(selectedValue)) {
                // устанавливаем флаг в true
                valueExists = true;
                return;
            }
        });
        // если выбранного значения нет в списке, добавляем его
        if (!valueExists) {
            createNewElement(selectedValue, container, listId, removeButtonClass, updateList);
        }
        // сбрасываем select на дефолтное значение
        select.selectedIndex = 0;
    });
}

// инициализуем секцию специализаций и регионов
const specializationsContainer = document.querySelector('#specializations');
initRemoveButtons(document.querySelectorAll('.remove-work'), 'specializations', updateWorksList);
initSelect('type_works', 'specializations', 'works', 'remove-work', updateWorksList);

const jobRegionsContainer = document.querySelector('#job_regions');
initRemoveButtons(document.querySelectorAll('.remove-region'), 'job_regions', updateRegionsList);
initSelect('work_regions', 'job_regions', 'regions', 'remove-region', updateRegionsList);

// функции обновления типов работ и регионов
function updateWorksList() {
    updateList('specializations', 'works');
}

function updateRegionsList() {
    updateList('job_regions', 'regions');
}


// функция обновляет данные компании
function updateData() {
  const button = document.querySelector('#update-company-data-btn');
  const specializationsCompany = document.querySelector('#specializations');
  const regionworkCompany = document.querySelector('#job_regions');

  button.addEventListener('click', () => {
    const updateUrl = `/users/company/edit/${company_pk}/update_data_company/`;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', updateUrl, true);

    // Получаем CSRF-токен из cookies
    const csrftoken = getCookie('csrftoken');

    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    // Добавляем заголовок X-CSRFToken в запрос
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    const specializations = Array.from(specializationsCompany.querySelectorAll('span'))
      .map(span => span.textContent.replace(/✕/g, ''))
      .filter(specialization => specialization !== '');

    const regions = Array.from(regionworkCompany.querySelectorAll('span'))
      .map(span => span.textContent.replace(/✕/g, ''))
      .filter(region => region !== '');

    const data = { type_works: specializations, region_works: regions };

    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        console.log(xhr.responseText);
        window.location.href = window.location.href;
      }
    };

    xhr.send(JSON.stringify(data));
  });
}

updateData();