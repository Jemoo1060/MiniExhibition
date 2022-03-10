
        // 로그인 페이지로
        function login_page() {
            window.location.href = "/loginpage"
        }

        // 글쓰기 페이지로
        function to_upload() {
            window.location.href = "/posting"
        }

        //로그아웃
        function logout() {
            $.removeCookie('mytoken',{path : '/'});
            window.location.href = "/"
        }

        // 메인페이지로
        function to_main() {
            window.location.href = "/"
        }

        // 댓글 등록
        function comment_upload(post_num) {
            let comment = $('#comment_text').val();

            if (comment == ''){
                alert('댓글을 작성해주세요')
                return
            }

            $.ajax({
                type: 'POST',
                url: '/comment',

                data: {'post_num_give': post_num, 'comment_give': comment},
                success: function (response) {
                    if(response['login_check'] == false){
                        alert('로그인 후 사용 가능한 기능입니다')
                    } else {
                        location.reload();
                    }

                }
            });
        }


        // 댓글 삭제
        function comment_setting(post_num, comment_num, comment_writer_id) {
            if (confirm('해당 댓글을 삭제 하시겠습니까?')) {
                $.ajax({
                    type: 'POST',
                    url: '/comment_cancel_check',

                    data: {
                        'comment_writer_id_give': comment_writer_id
                        , 'post_num_give': post_num,
                        'comment_num_give': comment_num
                    },
                    success: function (response) {

                        if (response['check']) {
                            location.reload();
                        } else {
                            alert('댓글 작성자만이 가능한 기능입니다')
                        }
                    }
                });
            } else {
                return;
            }
        }

        // 게시글 삭제
        function post_setting(post_num) {
            if (confirm('해당 댓글을 삭제 하시겠습니까?')) {
                $.ajax({
                    type: 'POST',
                    url: '/post_cancel',

                    data: {
                        'post_num_give': post_num
                    },
                    success: function (response) {
                        alert(response['msg'])
                        window.location.href = "/"
                    }
                });
            } else {
                return;
            }
        }