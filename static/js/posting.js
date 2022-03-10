
        // 메인페이지로
        function to_main() {
            window.location.href = "/"
        }

        //로그아웃
        function logout() {
            $.removeCookie('mytoken', {path: '/'});
            window.location.href = "/"
        }


        // 글 등록(image 업로드)
        function post_upload() {

            let file = $('#inputGroupFile04')[0].files[0]

            let pic_name = $('#pic_name').val();
            let pic_explain = $('#pic_explain').val();
            let file_chk = $('#inputGroupFile04').val();

            if (file_chk == '') {
                alert('올바른 파일을 첨부해주세요')
                return
            }

            if (pic_name == '') {
                $('#help_pic_name').show()
                $('#pic_name').focus()
                return
            }
            if (pic_explain == '') {
                $('#help_pic_explain').show()
                $('#pic_explain').focus()
                return
            }

            let form_data = new FormData()
            form_data.append("file_give", file)
            form_data.append("pic_name_give", pic_name)
            form_data.append("pic_explain_give", pic_explain)

            $.ajax({
                type: 'POST',
                url: '/posting/post',
                data: form_data,
                cache: false,
                contentType: false,
                processData: false,
                success: function (response) {
                    alert(response['msg'])
                    window.location.href = "/"
                }
            });
        }

        // 그림 미리보기(preview업로드)
        function update_profile() {
            let file_chk = $('#inputGroupFile04').val();
            if (file_chk != '') {
                let file = $('#inputGroupFile04')[0].files[0]
                let form_data = new FormData()
                form_data.append("file_give", file)

                $.ajax({
                    type: "POST",
                    url: "/update_profile",
                    data: form_data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {

                        if (response["result"] == "success") {
                            $('#cancelBtn').show();
                            $('#previewBtn').hide();
                            $('#image').show();
                            let temp = ` <img src="../static/preview/${response["filename"]}">`
                            $('#image').append(temp);
                        }
                    }
                });
            } else {
                alert('올바른 파일을 첨부해주세요')
            }

        }

        // 그림 미리보기 취소
        function picreset() {
            $('#inputGroupFile04').val('');
            $('#cancelBtn').hide();
            $('#previewBtn').show();
            $('#image').empty().hide();
        }