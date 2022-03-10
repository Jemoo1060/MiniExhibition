

        $(document).ready(function () {
            // 시작 회원가입 박스 숨기기
            $('#join_box').hide()
        });

        // 로그인 박스 숨기기, 회원가입 박스 표시
        function close_login_box() {
            $('#login_box').hide()
            $('#join_box').show()
        }

        // 회원가입 박스 숨기기, 로그인 박스 표시
        function close_join_box() {
            $('#join_box').hide()
            $('#login_box').show()
        }

        //로그인
        function sign_in() {
            let user_id = $("#login_id").val()
            let password = $("#login_pw").val()

            if (user_id == "") {
                $("#help-id-login").text("아이디를 입력해주세요.")
                $("#login_id").focus()
                return;
            } else {
                $("#help-id-login").text("")
            }

            if (password == "") {
                $("#help-password-login").text("비밀번호를 입력해주세요.")
                $("#input-password").focus()
                return;
            } else {
                $("#help-password-login").text("")
            }
            $.ajax({
                type: "POST",
                url: "/login",
                data: {
                    'user_id': user_id,
                    'pwd': password
                },
                success: function (response) {
                    if (response['result'] == 'success') {
                        $.cookie('mytoken', response['token'], {path: '/'});
                        window.location.href = "/"
                    } else {
                        alert(response['msg'])
                    }
                }
            });
        }

        // 회원가입
        function sign_up() {
            let username = $('#join_id').val()
            let password = $('#join_pw').val()
            let password2 = $('#join_chk_pw').val()


            if ($("#help-id").hasClass("is-danger")) {
                alert("아이디를 다시 확인해주세요.")
                return;
            } else if (!$("#help-id").hasClass("is-success")) {
                alert("아이디 중복확인을 해주세요.")
                return;
            }

            if (password == "") {
                $("#help-password").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
                $("#join_pw").focus()
                return;
            } else if (!is_password(password)) {
                $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").removeClass("is-safe").addClass("is-danger")
                $("#join_pw").focus()
                return
            } else {
                $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("is-danger").addClass("is-success")
            }
            if (password2 == "") {
                $("#help-password2").text("비밀번호를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
                $("#join_chk_pw").focus()
                return;
            } else if (password2 != password) {
                $("#help-password2").text("비밀번호가 일치하지 않습니다.").removeClass("is-safe").addClass("is-danger")
                $("#join_chk_pw").focus()
                return;
            } else {
                $("#help-password2").text("비밀번호가 일치합니다.").removeClass("is-danger").addClass("is-success")
            }
            $.ajax({
                type: "POST",
                url: "/join",
                data: {
                    'user_id': username,
                    'pwd': password
                },
                success: function (response) {
                    alert("회원가입을 축하드립니다!")
                    window.location.replace("")
                }
            });

        }

        // 아이디 중복 체크
        function check_dup() {
            let username = $("#join_id").val()

            if (username == "") {
                $("#help-id").text("아이디를 입력해주세요.").removeClass("is-safe").addClass("is-danger")
                $("#join_id").focus()
                return;
            }
            if (!is_nickname(username)) {
                $("#help-id").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이").removeClass("is-safe").addClass("is-danger")
                $("#join_id").focus()
                return;
            }
            $("#help-id").addClass("is-loading")
            $.ajax({
                type: "POST",
                url: "/check_dup",
                data: {
                    'user_id': username
                },
                success: function (response) {

                    if (response["exists"]) {
                        $("#help-id").text("이미 존재하는 아이디입니다.").removeClass("is-safe").addClass("is-danger")
                        $("#join_id").focus()
                    } else {
                        $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("is-danger").addClass("is-success")
                    }
                    $("#help-id").removeClass("is-loading")

                }
            });
        }

        // 아이디 생성조건 제약
        function is_nickname(asValue) {
            var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
            return regExp.test(asValue);
        }

        // 비밀번호 생성조건 제약
        function is_password(asValue) {
            var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
            return regExp.test(asValue);
        }

        // 메인페이지로
        function to_main() {
            window.location.href = "/"
        }

