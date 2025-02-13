Java.perform(function () {
    console.log('Hello, World!');
    let Builder = Java.use("okhttp3.CertificatePinner$Builder");
    Builder["add"].implementation = function (pattern, pins) {
        console.log(`Builder.add is called: pattern=${pattern}, pins=${pins}`);
        return this;
    };
})
