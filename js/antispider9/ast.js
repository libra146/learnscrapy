const fs = require('fs'); //导入需要的库
const parser = require("@babel/parser");
const types = require("@babel/types");
const traverse = require("@babel/traverse").default;
const generator = require("@babel/generator").default;

encodeFile = "encode.js";//定义输入以及输出文件
decodeFile = "decode.js";

//将源代码解析成 AST对象
let ast = parser.parse(fs.readFileSync(encodeFile, {encoding: "utf-8"}));


// 解密函数开始//
var n = ["qMfZzty0", "Dg9tDhjPBMC=", "y29UC3rYDwn0B3i=", "y29UC29Szq==", "E30Uy29UC3rYDwn0B3iOiNjLDhvYBIb0AgLZiIKOicK=", "CMv0DxjUicHMDw5JDgLVBIGPia==", "zw5J", "u0Hbmq==", "ChjVDg90ExbL", "AM9PBG==", "BgvUz3rO", "CgfYC2u=", "CM91BMq=", "zxjYB3i=", "C3rYAw5NAwz5", "xIHBxIbDkYGGk1TEif0RksSPk1TEif19", "DgvZDa==", "CMv0DxjUic8IicSGDgHPCYaRiciV", "ChvZAa==", "Aw5MBW==", "DgfIBgu=", "yMLUza==", "sgv4", "zxHJzxb0Aw9U", "x19WCM90B19F"];
(function (t, r) {
        var e = function (r) {
            while (--r)
                t["push"](t["shift"]())
        }
            , n = function () {
            var t = {
                data: {
                    key: "cookie",
                    value: "timeout"
                },
                setCookie: function (t, r, e, n) {
                    n = n || {};
                    for (var i = r + "=" + e, o = 0, c = t["length"]; o < c; o++) {
                        var a = t[o];
                        i += "; " + a;
                        var s = t[a];
                        t["push"](s),
                            c = t["length"],
                        !0 !== s && (i += "=" + s)
                    }
                    n["cookie"] = i
                },
                removeCookie: function () {
                    return "dev"
                },
                getCookie: function (t, n) {
                    t = t || function (t) {
                        return t
                    }
                    ;
                    var i = t(new RegExp("(?:^|; )" + n["replace"](/([.$?*|{}()[]\/+^])/g, "$1") + "=([^;]*)"))
                        , o = function (t, r) {
                        t(++r)
                    };
                    return o(e, r),
                        i ? decodeURIComponent(i[1]) : void 0
                }
            }
                , n = function () {
                var r = new RegExp("\\w+ *\\(\\) *{\\w+ *['|\"].+['|\"];? *}");
                return !r["test"](t["removeCookie"]["toString"]())
            };
            t["updateCookie"] = n;
            var i = t["updateCookie"]();
            i ? i ? t["getCookie"](null, "counter") : t["removeCookie"]() : t["setCookie"](["*"], "counter", 1)
        };
        n()
    }
)(n, 268);
var i = function (t, r) {
    t -= 0;
    var e = n[t];
    if (void 0 === i["YBXane"]) {
        var o = function (t) {
            for (var r, e, n = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=", i = String(t)["replace"](/=+$/, ""), o = "", c = 0, a = 0; e = i["charAt"](a++); ~e && (r = c % 4 ? 64 * r + e : e, c++ % 4) ? o += String["fromCharCode"](255 & r >> (-2 * c & 6)) : 0) e = n["indexOf"](e);
            return o;
        };
        i["hcXQrU"] = function (t) {
            for (var r = o(t), e = [], n = 0, i = r["length"]; n < i; n++) e += "%" + ("00" + r["charCodeAt"](n)["toString"](16))["slice"](-2);
            return decodeURIComponent(e);
        }, i["qaIbTt"] = {}, i["YBXane"] = !0;
    }
    var c = i["qaIbTt"][t];
    if (void 0 === c) {
        var a = function (t) {
            this["UPosFF"] = t, this["uNCitX"] = [1, 0, 0], this["scGwKU"] = function () {
                return "newState";
            }, this["GuVesY"] = "\\w+ *\\(\\) *{\\w+ *", this["eAEAZh"] = "['|\"].+['|\"];? *}";
        };
        a["prototype"]["YGAmBh"] = function () {
            var t = new RegExp(this["GuVesY"] + this["eAEAZh"]),
                r = !t["test"](this["scGwKU"]["toString"]()) ? --this["uNCitX"][1] : --this["uNCitX"][0];
            return this["fRxEcE"](r);
        }, a["prototype"]["fRxEcE"] = function (t) {
            return Boolean(~t) ? this["VYShKn"](this["UPosFF"]) : t;
        }, a["prototype"]["VYShKn"] = function (t) {
            for (var r = 0, e = this["uNCitX"]["length"]; r < e; r++) this["uNCitX"]["push"](Math["round"](Math["random"]())), e = this["uNCitX"]["length"];
            return t(this["uNCitX"][0]);
        }, new a(i)["YGAmBh"](), e = i["hcXQrU"](e), i["qaIbTt"][t] = e;
    } else e = c;
    return e;
}
//解密函数结束//


traverse(ast, {
    CallExpression(path) {
        let {node} = path;
        //别忘了判断一下是不是我们要的函数，如果不是我们需要，则直接返回不做任何处理，不然会破坏其他正常的函数
        if (node.arguments.length === 1 && types.isStringLiteral(node.arguments[0]) && node.arguments[0].value.indexOf('0x') !== -1) {
            let args = node.arguments[0].value; //获取函数参数，例如：0x30
            console.log(args);
            let result = i(args)//调用实际的解密函数
            console.log(result)
            path.replaceWith(types.stringLiteral(result));//构造一个字符串节点，替换原来的节点
        }
    }
});


//将 AST 语法树还原成代码
let {code} = generator(ast, opts = {
    "jsescOption": {"minimal": true},
});
//将生成好的代码写入新的文件
fs.writeFile(decodeFile, code, (err) => {
});
