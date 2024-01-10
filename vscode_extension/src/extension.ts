import * as vscode from 'vscode';
import { OptionsViewProvider } from './pages/options';
import { PromptPlaygroundPage } from './pages/playground';
import { TmplEditorViewProvider } from './pages/tmpl_editor';
import { RetrievalEditorViewProvider } from './pages/retrieval_editor';

export function activate(context: vscode.ExtensionContext) {
	context.subscriptions.push(
        vscode.commands.registerCommand("pp.playground", async () => {
            new PromptPlaygroundPage().display(context);
        })
    );
    // if (vscode.env.isNewAppInstall) {
    //     vscode.commands.executeCommand("pp.playground");
    // }

    let optionsProvider = new OptionsViewProvider();
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(
            OptionsViewProvider.viewType, optionsProvider));

    let tmplEditorProvider = new TmplEditorViewProvider();
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(
        TmplEditorViewProvider.viewType, tmplEditorProvider));
    let retrievalEditorProvider = new RetrievalEditorViewProvider();
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(
        RetrievalEditorViewProvider.viewType, retrievalEditorProvider));
}

export function deactivate() {}
