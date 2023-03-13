// календарь формы
function initDatepickers(sroDate, licenseDate) {
    $("#sro_date").datepicker({
        dateFormat: "yy-mm-dd"
    }).datepicker("setDate", new Date(sroDate));

    $("#license_date").datepicker({
        dateFormat: "yy-mm-dd"
    }).datepicker("setDate", new Date(licenseDate));
}


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

// удаление сотрудника
$(document).ready(function () {
    $('#confirm-delete-employee-modal').on('show.bs.modal', function (e) {
        let employeePk = $(e.relatedTarget).data('employee-pk');
        let deleteUrl = $(e.relatedTarget).data('delete-url');
        $('#confirm-delete-btn').data('employee-pk', employeePk);
        $('#confirm-delete-btn').data('delete-url', deleteUrl);
    });

    $('#confirm-delete-btn').click(function () {
        let employeePk = $(this).data('employee-pk');
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
                    // window.location.href = editCompanyUrl;
                    $('#confirm-delete-employee-modal').modal('hide');
                    location.reload();
                }
            }
        });
    });
});


// добавить сотрудника
$(document).ready(function () {
    const addEmployeeForm = $('#add-employee-modal-form');
    const addEmployeeModal = $('#add-employee-modal');

    // Обработчик ошибок при отправке данных на сервер
    function handleErrors(xhr) {
        let errors = JSON.parse(xhr.responseText).errors;
        if (errors) {
            console.log(errors)
            // Выводим ошибки валидации, если они есть
            $.each(errors, function (key, value) {
                $("#" + "add-employee-" + key + "-error").text(value).show();
            });
        } else {
            // Выводим общее сообщение об ошибке
            alert('Произошла ошибка при добавлении сотрудника');
        }
    }

    // Обработчик успешной отправки данных на сервер
    function handleSuccess(data) {
        // Закрываем модальное окно, очищаем форму и обновляем страницу
        addEmployeeModal.modal('hide');
        addEmployeeForm[0].reset();
        location.reload();
    }

    // Функция, которая отправляет данные формы на сервер через AJAX-запрос
    function addEmployee() {
        $.ajax({
            url: `/users/company/edit/${company_pk}/add_employee/`,
            method: 'POST',
            data: addEmployeeForm.serialize(),
            success: handleSuccess,
            error: handleErrors
        });
    }

    // Очищаем сообщения об ошибках при каждом новом открытии формы
    addEmployeeModal.on('hidden.bs.modal', function () {
        $(".error-message").text("").hide();
    });

    // Отправляем данные формы на сервер при отправке формы
    addEmployeeForm.submit(function (event) {
        event.preventDefault();
        $(".error-message").hide();
        addEmployee();
    });
});


// редактировать сотрудника
$(document).on('click', '.edit-employee-btn', function () {
    let employee_pk = $(this).data('employee-pk');
    let update_url = $(this).data('update-url');
    let modal = $('#edit-employee-modal');

    $.ajax({
        url: `/users/get_employee_data/${employee_pk}/`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            modal.find('#position').val(data.position);
            modal.find('#surname').val(data.surname);
            modal.find('#name').val(data.name);
            modal.find('#father_name').val(data.father_name);
            modal.find('form').attr('action', update_url);
        }
    });

    modal.find('form').off('submit').on('submit', function (e) {
        e.preventDefault();
        let form = $(this);

        // Обработчик ошибок при отправке данных на сервер
        function handleErrors(xhr) {
            let errors = JSON.parse(xhr.responseText).errors;
            if (errors) {
                // Выводим ошибки валидации, если они есть
                $.each(errors, function (key, value) {
                    $("#" + "edit-employee-" + key + "-error").text(value).show();
                });
            } else {
                // Выводим общее сообщение об ошибке
                alert('Произошла ошибка при обновлении данных сотрудника');
            }
        }

        // Обработчик успешной отправки данных на сервер
        function handleSuccess(data) {
            modal.modal('hide');
            location.reload();
        }

        // Функция, которая отправляет данные формы на сервер через AJAX-запрос
        function updateEmployee() {
            $.ajax({
                url: update_url,
                type: 'POST',
                data: form.serialize(),
                dataType: 'json',
                success: handleSuccess,
                error: handleErrors
            });
        }

        // Очищаем сообщения об ошибках при каждом новом открытии формы
        modal.on('hidden.bs.modal', function () {
            $(".error-message").text("").hide();
        });

        // Отправляем данные формы на сервер при отправке формы
        $(".error-message").hide();
        updateEmployee();
    });
});