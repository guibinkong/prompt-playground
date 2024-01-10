import * as vscode from "vscode";
import { WebviewPage, WEBVIEW_OPTIONS } from "./page";
import { getWebViewHtml } from "./page_template"

const TEMPLATE = `
<iframe width="96%" height="800px" src="https://prompt-fe.appspot.com/options?iframed=1" title="">
</iframe>
`;


const VIEW_TYPE = 'pp.llm_options';
export class OptionsPage extends WebviewPage {
    protected title: string = 'Settings';

    public constructor() {
        super(VIEW_TYPE)
    }

    public renderContent(): string {
        return TEMPLATE;
    }
}

export class OptionsViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = VIEW_TYPE;

    public resolveWebviewView(webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext, _token: vscode.CancellationToken,) {
            webviewView.webview.options = WEBVIEW_OPTIONS;
            webviewView.webview.html = getWebViewHtml(new OptionsPage().renderContent());

            vscode.commands.executeCommand("pp.playground");
    }
}
