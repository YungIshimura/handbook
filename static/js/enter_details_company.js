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


/* Блок выбора типов работ, выполняемых организацией */
function handleRemoveButtonClick(button, specializationsDiv) {
    // Получаем родительский элемент кнопки - <span>
    const span = button.parentNode;
    // Удаляем элемент <span> из <div>
    specializationsDiv.removeChild(span);
    // Обновляем список работ в <div> с id="works"
    updateWorksList();
}

function addNewSpecialization(selectedWork, specializationsDiv) {
    const newSpan = document.createElement('span');
    newSpan.textContent = selectedWork;
    const removeButton = document.createElement('span');
    removeButton.classList.add('remove-work');
    removeButton.textContent = '✕';
    newSpan.appendChild(removeButton);
    specializationsDiv.appendChild(newSpan);

    // Добавляем обработчик клика на кнопку удаления
    removeButton.addEventListener('click', () => {
        handleRemoveButtonClick(removeButton, specializationsDiv);
    });

    // Обновляем список работ в <div> с id="works"
    updateWorksList();
}

function updateWorksList() {
    const specializationsDiv = document.querySelector('#specializations');
    const worksList = document.querySelector('#works');
    // Очищаем список работ компании
    worksList.innerHTML = '';
    // Получаем список всех работ в <div> с id="works"
    const specializations = specializationsDiv.querySelectorAll('span');
    // Проходимся по всем работам и добавляем их в список работ компании
    specializations.forEach(span => {
        const work = span.textContent;
        const li = document.createElement('li');
        li.textContent = work;
        worksList.appendChild(li);
    });
}

// Получаем список элементов с классом 'remove-work'
const removeButtons = document.querySelectorAll('.remove-work');

// Добавляем обработчик клика на каждую кнопку
removeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const specializationsDiv = document.querySelector('#specializations');
        handleRemoveButtonClick(button, specializationsDiv);
    });
});

const select = document.querySelector('#type_works');
const specializationsDiv = document.querySelector('#specializations');

select.addEventListener('change', () => {
    // Получаем выбранную работу из <select>
    const selectedWork = select.value;
    // Получаем список всех работ в <div> с id="specializations"
    const specializations = specializationsDiv.querySelectorAll('span');

    // Проходимся по всем работам и проверяем, есть ли выбранная работа
    let workExists = false;
    specializations.forEach(span => {
        if (span.textContent.includes(selectedWork)) {
            workExists = true;
            return;
        }
    });

    // Если выбранной работы еще нет, добавляем ее в <div>
    if (!workExists) {
        addNewSpecialization(selectedWork, specializationsDiv);
    }
});

// редактировать сотрудника
// $(document).on('click', '.edit-employee-btn', function () {
//     let employee_pk = $(this).data('employee-pk');
//     let update_url = $(this).data('update-url');
//     let modal = $('#edit-employee-modal');
//
//     $.ajax({
//         url: `/users/get_employee_data/${employee_pk}/`,
//         type: 'GET',
//         dataType: 'json',
//         success: function (data) {
//             modal.find('#position').val(data.position);
//             modal.find('#surname').val(data.surname);
//             modal.find('#name').val(data.name);
//             modal.find('#father_name').val(data.father_name);
//             modal.find('#phonenumber').val(data.phonenumber);
//             modal.find('#email').val(data.email);
//             modal.find('form').attr('action', update_url);
//         }
//     });
//
//     modal.find('form').off('submit').on('submit', function (e) {
//         e.preventDefault();
//         let form = $(this);
//
//         // Обработчик ошибок при отправке данных на сервер
//         function handleErrors(xhr) {
//             let errors = JSON.parse(xhr.responseText).errors;
//             if (errors) {
//                 // Выводим ошибки валидации, если они есть
//                 $.each(errors, function (key, value) {
//                     $("#" + "edit-employee-" + key + "-error").text(value).show();
//                 });
//             } else {
//                 // Выводим общее сообщение об ошибке
//                 alert('Произошла ошибка при обновлении данных сотрудника');
//             }
//         }
//
//         // Обработчик успешной отправки данных на сервер
//         function handleSuccess(data) {
//             modal.modal('hide');
//             location.reload();
//         }
//
//         // Функция, которая отправляет данные формы на сервер через AJAX-запрос
//         function updateEmployee() {
//             $.ajax({
//                 url: update_url,
//                 type: 'POST',
//                 data: form.serialize(),
//                 dataType: 'json',
//                 success: handleSuccess,
//                 error: handleErrors
//             });
//         }
//
//         // Очищаем сообщения об ошибках при каждом новом открытии формы
//         modal.on('hidden.bs.modal', function () {
//             $(".error-message").text("").hide();
//         });
//
//         // Отправляем данные формы на сервер при отправке формы
//         $(".error-message").hide();
//         updateEmployee();
//     });
// });
//
//
// // редактировать филиал
// $(document).on('click', '.edit-branches-btn', function () {
//     let branche_pk = $(this).data('branche-pk');
//     let update_url = $(this).data('update-url');
//     let modal = $('#edit-branches-modal');
//
//     $.ajax({
//         url: `/users/get_branche_data/${branche_pk}/`,
//         type: 'GET',
//         dataType: 'json',
//         success: function (data) {
//             modal.find('#region').val(data.region);
//             modal.find('#postcode').val(data.postcode);
//             modal.find('#name').val(data.city);
//             modal.find('#district').val(data.district);
//             modal.find('#street').val(data.street);
//             modal.find('#house_number').val(data.house_number);
//             modal.find('form').attr('action', update_url);
//         }
//     });
//
//     modal.find('form').off('submit').on('submit', function (e) {
//         e.preventDefault();
//         let form = $(this);
//
//         // Обработчик ошибок при отправке данных на сервер
//         function handleErrors(xhr) {
//             let errors = JSON.parse(xhr.responseText).errors;
//             if (errors) {
//                 // Выводим ошибки валидации, если они есть
//                 $.each(errors, function (key, value) {
//                     $("#" + "edit-branches-" + key + "-error").text(value).show();
//                 });
//             } else {
//                 // Выводим общее сообщение об ошибке
//                 alert('Произошла ошибка при обновлении данных сотрудника');
//             }
//         }
//
//         // Обработчик успешной отправки данных на сервер
//         function handleSuccess(data) {
//             modal.modal('hide');
//             location.reload();
//         }
//
//         // Функция, которая отправляет данные формы на сервер через AJAX-запрос
//         function updateBranche() {
//             $.ajax({
//                 url: update_url,
//                 type: 'POST',
//                 data: form.serialize(),
//                 dataType: 'json',
//                 success: handleSuccess,
//                 error: handleErrors
//             });
//         }
//
//         // Очищаем сообщения об ошибках при каждом новом открытии формы
//         modal.on('hidden.bs.modal', function () {
//             $(".error-message").text("").hide();
//         });
//
//         // Отправляем данные формы на сервер при отправке формы
//         $(".error-message").hide();
//         updateBranche();
//     });
// });


// добавить сотрудника
// $(document).ready(function () {
//     const addEmployeeForm = $('#add-employee-modal-form');
//     const addEmployeeModal = $('#add-employee-modal');
//
//     // Обработчик ошибок при отправке данных на сервер
//     function handleErrors(xhr) {
//         let errors = JSON.parse(xhr.responseText).errors;
//         if (errors) {
//             console.log(errors)
//             // Выводим ошибки валидации, если они есть
//             $.each(errors, function (key, value) {
//                 $("#" + "add-employee-" + key + "-error").text(value).show();
//             });
//         } else {
//             // Выводим общее сообщение об ошибке
//             alert('Произошла ошибка при добавлении сотрудника');
//         }
//     }
//
//     // Обработчик успешной отправки данных на сервер
//     function handleSuccess(data) {
//         // Закрываем модальное окно, очищаем форму и обновляем страницу
//         addEmployeeModal.modal('hide');
//         addEmployeeForm[0].reset();
//         location.reload();
//     }
//
//     // Функция, которая отправляет данные формы на сервер через AJAX-запрос
//     function addEmployee() {
//         $.ajax({
//             url: `/users/company/edit/${company_pk}/add_employee/`,
//             method: 'POST',
//             data: addEmployeeForm.serialize(),
//             success: handleSuccess,
//             error: handleErrors
//         });
//     }
//
//     // Очищаем сообщения об ошибках при каждом новом открытии формы
//     addEmployeeModal.on('hidden.bs.modal', function () {
//         $(".error-message").text("").hide();
//     });
//
//     // Отправляем данные формы на сервер при отправке формы
//     addEmployeeForm.submit(function (event) {
//         event.preventDefault();
//         $(".error-message").hide();
//         addEmployee();
//     });
// });

// добавить филиал
// $(document).ready(function () {
//     const addBranchesForm = $('#add-branches-modal-form');
//     const addBranchesModal = $('#add-branches-modal');
//
//     // Обработчик ошибок при отправке данных на сервер
//     function handleErrors(xhr) {
//         let errors = JSON.parse(xhr.responseText).errors;
//         if (errors) {
//             console.log(errors)
//             // Выводим ошибки валидации, если они есть
//             $.each(errors, function (key, value) {
//                 console.log(key);
//                 $("#" + "add-branches-" + key + "-error").text(value).show();
//             });
//         } else {
//             // Выводим общее сообщение об ошибке
//             alert('Произошла ошибка при добавлении филиала');
//         }
//     }
//
//     // Обработчик успешной отправки данных на сервер
//     function handleSuccess(data) {
//         // Закрываем модальное окно, очищаем форму и обновляем страницу
//         addBranchesModal.modal('hide');
//         addBranchesForm[0].reset();
//         location.reload();
//     }
//
//     // Функция, которая отправляет данные формы на сервер через AJAX-запрос
//     function addBranches() {
//         $.ajax({
//             url: `/users/company/edit/${company_pk}/add_branch/`,
//             method: 'POST',
//             data: addBranchesForm.serialize(),
//             success: handleSuccess,
//             error: handleErrors
//         });
//     }
//
//     // Очищаем сообщения об ошибках при каждом новом открытии формы
//     addBranchesModal.on('hidden.bs.modal', function () {
//         $(".error-message").text("").hide();
//     });
//
//     // Отправляем данные формы на сервер при отправке формы
//     addBranchesForm.submit(function (event) {
//         event.preventDefault();
//         $(".error-message").hide();
//         addBranches();
//     });
// })