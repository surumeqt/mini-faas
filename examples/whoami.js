function hello(event) {
    const name = event.name
    return {
        message: "hello " + name
    };
}

module.exports = {
    hello
};