const fs = require('fs'); //导入需要的库
const parser = require("@babel/parser");
const types = require("@babel/types");
const traverse = require("@babel/traverse").default;
const generator = require("@babel/generator").default;

encodeFile = "main.js";//定义输入以及输出文件
decodeFile = "main_decode.js";

//将源代码解析成 AST对象
let ast = parser.parse(fs.readFileSync(encodeFile, {encoding: "utf-8"}));

//修改 AST 语法树
let hex_decode = {
    //遍历说中的字符串节点，只需要写一遍，框架会自动遍历所有的节点
    StringLiteral({node}) {
        if (node.value !== node.extra.raw) {
            node.extra.raw = "'" + node.value + "'";
        }
    },
}
//执行实际的修改
traverse(ast, hex_decode);

// 解密函数开始//
const _0x4afa = ['1993-03-11', '79.4KG', '1984-05-29', 'stringify', '128.8KG', '1991-06-29', '198cm', 'davis.png', '208cm', '卡尔-安东尼-唐斯', '188cm', '196cm', 'antetokounmpo.png', '83.9KG', '112.5KG', 'toString', 'embiid.png', '88.5KG', '114.8KG', '203cm', '206cm', '斯蒂芬-库里', '1988-03-14', 'JD8wgBMgVjdQbBUVbMarpZMAadLD7yvfzVV', 'Base64', '考瓦伊-莱昂纳德', '扬尼斯-安特托昆博', 'leonard.png', '安东尼-戴维斯', '达米安-利拉德', '109.8KG', 'harden.png', '99.8KG', 'durant.png', '102.1KG', 'paul.png', '1989-08-26', '1985-05-06', 'key', 'parse', '201cm', '113.4KG', '108.9KG', '1988-11-12', 'Utf8', '90.7KG', '尼科拉-约基奇', '213cm', 'pad', 'enc', '卡梅罗-安东尼', 'westbrook.png', 'encrypt', '127.0KG', 'thompson.png', '1994-12-06', 'irving.png', '185cm', 'lillard.png', '拉塞尔-威斯布鲁克', '1990-02-08', 'anthony.png', '191cm'];
(function (_0x35db0b, _0x4afab2) {
    const _0x343162 = function (_0x6f5802) {
        while (--_0x6f5802) {
            _0x35db0b['push'](_0x35db0b['shift']());
        }
    };
    _0x343162(++_0x4afab2);
})(_0x4afa, 0xed);
const _0x3431 = function (_0x35db0b, _0x4afab2) {
    _0x35db0b = _0x35db0b - 0x0;
    let _0x343162 = _0x4afa[_0x35db0b];
    return _0x343162;
};
//解密函数结束//


traverse(ast, {
    CallExpression(path) {
        let {node} = path;
        //别忘了判断一下是不是我们要的函数，如果不是我们需要，则直接返回不做任何处理，不然会破坏其他正常的函数
        if (node.arguments.length !== 1 || node.callee.name !== '_0x5e920f') {
            return;
        }
        let args = node.arguments[0].value; //获取函数参数，例如：0x30
        let result = _0x3431(args)//调用实际的解密函数
        console.log(result)
        path.replaceWith(types.stringLiteral(result));//构造一个字符串节点，替换原来的节点
    }
});

//删除 NewExpression节点
traverse(ast, {
    NewExpression(path) {
        path.remove();
    }
})

//将 AST 语法树还原成代码
let {code} = generator(ast, opts = {
    "jsescOption": {"minimal": true},
});
//将生成好的代码写入新的文件
fs.writeFile(decodeFile, code, (err) => {
});
