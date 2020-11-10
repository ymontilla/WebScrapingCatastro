var args = process.argv;

const CDP = require('chrome-remote-interface');

async function navigateInANewTab(url) {
    const tab = await CDP.New();
    const client = await CDP({tab});
    const {Page} = client;
    await Page.enable();
    await Page.navigate({url});
    await Page.loadEventFired();
    await new Promise(resolve => setTimeout(resolve, 5000));
    await CDP.Close({id: tab.id});
}

navigateInANewTab(args[2])
