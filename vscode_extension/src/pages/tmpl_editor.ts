import * as vscode from "vscode";
import { WebviewPage, WEBVIEW_OPTIONS } from "./page";
import { getWebViewHtml } from "./page_template"

const TEMPLATE = `
<iframe width="96%" height="800px" src="https://prompt-fe.appspot.com/template_editor?iframed=1" title="">
</iframe>
`;


const VIEW_TYPE = 'pp.tmpl_editor';
export class TmplEditorPage extends WebviewPage {
    protected title: string = 'Templates';

    public constructor() {
        super(VIEW_TYPE)
    }

    public renderContent(): string {
        return TEMPLATE;
    }
}

export class TmplEditorViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = VIEW_TYPE;

    public resolveWebviewView(webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext, _token: vscode.CancellationToken,) {
            webviewView.webview.options = WEBVIEW_OPTIONS;
            webviewView.webview.html = getWebViewHtml(new TmplEditorPage().renderContent());

            vscode.commands.executeCommand("pp.playground");
    }
}
