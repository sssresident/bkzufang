/*定义验证规则*/
const isnum = /^[0-9]*$/;
const isphone = /^[1][3,4,5,6,7,8,9][0-9]{9}$/;
const ismail = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
const issfz = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;


/*混入*/
const myMixin = {
    methods: {
        handleEdit(title,url, width, height) {

            xadmin.open(title, url, width, height)
        },
        handleEditadd(title,url) {

            xadmin.add_tab(title,url)
        },
        handleEditall(url) {

            xadmin.open('编辑', url, '', '', true)
        }


    },
    computed: {
        //计算分页属性
        indexs: function () {
            var left = 1;
            var right = this.all;
            var ar = [];
            if (this.all >= 5) {
                if (this.cur > 3 && this.cur < this.all - 2) {
                    left = this.cur - 2
                    right = this.cur + 2
                } else {
                    if (this.cur <= 3) {
                        left = 1
                        right = 5
                    } else {
                        right = this.all
                        left = this.all - 4
                    }
                }
            }
            while (left <= right) {
                ar.push(left)
                left++
            }
            return ar
        }
    }
}


/*定义页面app*/
const App = {
    delimiters: ["{[", "]}"], // 可自定义符号
    data() {
        return {
            message: '欢迎使用！'
        }
    }
}


//
// myapp.use(ElementPlus);
