        // 로그인 페이지로
        function login_page() {
            window.location.href = "/loginpage"
        }

        // 글 등록 페이지로
        function to_upload() {
            window.location.href = "/posting"
        }

        //로그아웃
        function logout() {
            $.removeCookie('mytoken', {path: '/'});
            window.location.href = "/"
        }

        // 메인페이지로
        function to_main() {
            window.location.href = "/"
        }

        // 상세 게시글로
        function to_detailPost(post_num) {
            window.location.href = "/detailPost/" + post_num
        }

        // 검색 기능 사용
        function select_post() {

            let pic_name = $('#select_input').val()

            if (pic_name == '') {
                alert('검색어를 적어주세요')
                return
            }
             window.location.href = "/select/" + pic_name
        }

