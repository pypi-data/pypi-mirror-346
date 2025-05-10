"use strict";
(self["webpackChunkjupyt"] = self["webpackChunkjupyt"] || []).push([["lib_index_js"],{

/***/ "./lib/components/cell-approval-controls.js":
/*!**************************************************!*\
  !*** ./lib/components/cell-approval-controls.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CellApprovalControls: () => (/* binding */ CellApprovalControls)
/* harmony export */ });
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Typography/Typography.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Paper/Paper.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Button/Button.js");
/* harmony import */ var react_diff_view__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-diff-view */ "./node_modules/react-diff-view/es/index.js");
/* harmony import */ var react_diff_view_style_index_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-diff-view/style/index.css */ "./node_modules/react-diff-view/style/index.css");
/* harmony import */ var _mui_material_styles__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/styles */ "./node_modules/@mui/material/esm/styles/useTheme.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);





/**
 * React component rendered within a cell to show pending operation details (diff/preview)
 * and provide Approve/Reject buttons.
 */
function CellApprovalControls({ pendingOperation, onApprove, onReject }) {
    const theme = (0,_mui_material_styles__WEBPACK_IMPORTED_MODULE_2__["default"])();
    const { type, code, oldCode, runNeeded } = pendingOperation;
    const renderDiff = () => {
        if (type === 'update_cell' && typeof code === 'string') {
            const currentOldCode = oldCode || '';
            const newLines = code.split('\n');
            const oldLines = currentOldCode.split('\n');
            const diffText = [
                '--- a/Original',
                '+++ b/Proposed',
                '@@ -1,' + oldLines.length + ' +1,' + newLines.length + ' @@',
                ...oldLines.map(line => '-' + line),
                ...newLines.map(line => '+' + line)
            ].join('\n');
            try {
                const files = (0,react_diff_view__WEBPACK_IMPORTED_MODULE_3__.parseDiff)(diffText);
                if (!(files === null || files === void 0 ? void 0 : files[0])) {
                    return null;
                }
                return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: {
                        border: '1px solid',
                        borderColor: 'divider',
                        borderRadius: 1,
                        overflow: 'hidden',
                        mb: 1,
                        '& .diff': {
                            fontSize: '0.9em',
                            color: theme.palette.text.primary,
                            backgroundColor: theme.palette.mode === 'dark'
                                ? '#1a1a1a'
                                : theme.palette.background.paper
                        },
                        '& .diff-gutter': {
                            backgroundColor: theme.palette.mode === 'dark' ? '#252525' : '#f0f0f0',
                            color: theme.palette.mode === 'dark' ? '#888' : '#666',
                            padding: '0 8px'
                        },
                        '& .diff-code': {
                            color: theme.palette.text.primary,
                            padding: '0 8px'
                        },
                        '& .diff-code-delete': {
                            backgroundColor: theme.palette.mode === 'dark'
                                ? 'rgba(255, 100, 100, 0.15)'
                                : '#ffeef0',
                            color: theme.palette.mode === 'dark' ? '#ff9999' : '#cc0000'
                        },
                        '& .diff-code-insert': {
                            backgroundColor: theme.palette.mode === 'dark'
                                ? 'rgba(133, 255, 133, 0.15)'
                                : '#e6ffec',
                            color: theme.palette.mode === 'dark' ? '#85ff85' : '#007700'
                        },
                        '& .diff-gutter-delete': {
                            backgroundColor: theme.palette.mode === 'dark' ? '#402020' : '#fff0f0'
                        },
                        '& .diff-gutter-insert': {
                            backgroundColor: theme.palette.mode === 'dark' ? '#204020' : '#f0fff0'
                        },
                        '& .diff-hunk-header': {
                            backgroundColor: theme.palette.mode === 'dark' ? '#303030' : '#f8f8f8',
                            color: theme.palette.mode === 'dark' ? '#888' : '#666'
                        }
                    } },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement(react_diff_view__WEBPACK_IMPORTED_MODULE_3__.Diff, { viewType: "unified", diffType: files[0].type, hunks: files[0].hunks, optimizeSelection: true, gutterType: "anchor" })));
            }
            catch (error) {
                console.error('Error parsing diff for cell approval:', error);
                return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { color: "error", variant: "body2" }, "Error displaying diff. Please check console."));
            }
        }
        return null;
    };
    const renderCodePreview = () => {
        if (type === 'create_cell' && code) {
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { component: _mui_material__WEBPACK_IMPORTED_MODULE_6__["default"], variant: "outlined", sx: {
                    p: 1.5,
                    mb: 1,
                    bgcolor: theme.palette.mode === 'dark'
                        ? 'rgba(133, 255, 133, 0.1)'
                        : '#e6ffec',
                    fontFamily: 'monospace',
                    whiteSpace: 'pre-wrap',
                    overflowX: 'auto',
                    fontSize: '0.9em',
                    color: theme.palette.mode === 'dark' ? '#85ff85' : '#007700',
                    border: '1px solid',
                    borderColor: theme.palette.mode === 'dark'
                        ? 'rgba(133, 255, 133, 0.2)'
                        : '#b0eab5'
                } }, code));
        }
        return null;
    };
    const renderDeleteOverlay = () => {
        if (type === 'delete_cell') {
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: {
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    bgcolor: theme.palette.mode === 'dark'
                        ? 'rgba(255, 100, 100, 0.15)'
                        : '#ffeef0',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    p: 2,
                    border: '1px dashed',
                    borderColor: theme.palette.mode === 'dark' ? '#ff9999' : '#cc0000',
                    borderRadius: 1,
                    zIndex: 5
                } },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { color: theme.palette.mode === 'dark' ? '#ff9999' : '#cc0000', variant: "h6" }, "Marked for Deletion")));
        }
        return null;
    };
    const getOperationTitle = () => {
        switch (type) {
            case 'create_cell':
                return 'Approve Cell Creation?';
            case 'update_cell':
                return 'Approve Cell Update?';
            case 'delete_cell':
                return 'Approve Cell Deletion?';
            default:
                return 'Approve Operation?';
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: {
            border: '2px dashed',
            borderColor: 'primary.main',
            p: 1.5,
            borderRadius: 1,
            position: 'relative',
            mb: 1,
            bgcolor: theme.palette.mode === 'dark'
                ? 'rgba(255, 255, 255, 0.03)'
                : 'rgba(0, 0, 0, 0.02)',
            color: theme.palette.text.primary
        } },
        renderDeleteOverlay(),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "subtitle1", gutterBottom: true, sx: {
                fontWeight: 'bold',
                color: theme.palette.mode === 'dark'
                    ? theme.palette.primary.light
                    : theme.palette.primary.main
            } }, getOperationTitle()),
        type === 'update_cell' ? renderDiff() : renderCodePreview(),
        runNeeded && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "caption", display: "block", sx: {
                mb: 1,
                fontStyle: 'italic',
                color: theme.palette.mode === 'dark'
                    ? theme.palette.grey[400]
                    : theme.palette.grey[700]
            } }, "Note: This cell will be executed after approval.")),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { display: 'flex', gap: 1, justifyContent: 'flex-end' } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_7__["default"], { size: "small", variant: "contained", color: "primary", onClick: onApprove }, "Approve"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_7__["default"], { size: "small", variant: "outlined", color: "error", onClick: onReject }, "Reject"))));
}


/***/ }),

/***/ "./lib/components/chat-header.js":
/*!***************************************!*\
  !*** ./lib/components/chat-header.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatHeader: () => (/* binding */ ChatHeader)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Typography/Typography.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Tooltip/Tooltip.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/IconButton/IconButton.js");
/* harmony import */ var _mui_icons_material_Add__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/icons-material/Add */ "./node_modules/@mui/icons-material/esm/Add.js");



function ChatHeader({ isStreaming, currentType, onNewChat, onModelConfigChange }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { py: 2 } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: 2
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "h4", component: "h1", sx: {
                    fontWeight: 600,
                    color: 'text.primary',
                    letterSpacing: '-0.5px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1
                } }, "Jupyt"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { display: 'flex', gap: 2, alignItems: 'center' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { title: "Start new chat" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { onClick: onNewChat, disabled: isStreaming, size: "small", sx: {
                            bgcolor: 'primary.main',
                            color: 'primary.contrastText',
                            '&:hover': {
                                bgcolor: 'primary.dark'
                            },
                            '&.Mui-disabled': {
                                bgcolor: 'action.disabledBackground',
                                color: 'action.disabled'
                            }
                        } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Add__WEBPACK_IMPORTED_MODULE_5__["default"], null))))),
        isStreaming && currentType && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__["default"], { variant: "body2", sx: {
                color: 'text.secondary',
                mt: 0.5,
                fontWeight: 400
            } }, currentType === 'simple_query'
            ? 'Processing Query'
            : 'Agent Planning'))));
}


/***/ }),

/***/ "./lib/components/chat-input.js":
/*!**************************************!*\
  !*** ./lib/components/chat-input.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatInput: () => (/* binding */ ChatInput)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/TextField/TextField.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/IconButton/IconButton.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/CircularProgress/CircularProgress.js");
/* harmony import */ var _mui_icons_material_Send__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/icons-material/Send */ "./node_modules/@mui/icons-material/esm/Send.js");
/* harmony import */ var _mui_icons_material_Stop__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/icons-material/Stop */ "./node_modules/@mui/icons-material/esm/Stop.js");




function ChatInput({ value, isStreaming, onChange, onSubmit, isAgenticLooping, onStopAgenticLoop }) {
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const handleCellSelected = (event) => {
            const cellInfo = event.detail;
            const cellRef = `@cell${cellInfo.cellNumber} `;
            // If there's already text, add the cell reference at the cursor position
            if (inputRef.current) {
                const cursorPos = inputRef.current.selectionStart || 0;
                const currentValue = value;
                const newValue = currentValue.slice(0, cursorPos) +
                    cellRef +
                    currentValue.slice(cursorPos);
                onChange(newValue);
                // Set cursor position after the cell reference
                setTimeout(() => {
                    if (inputRef.current) {
                        const newCursorPos = cursorPos + cellRef.length;
                        inputRef.current.setSelectionRange(newCursorPos, newCursorPos);
                        inputRef.current.focus();
                    }
                }, 0);
            }
            else {
                onChange(cellRef);
            }
        };
        document.addEventListener('jupyt:cell-selected', handleCellSelected);
        return () => {
            document.removeEventListener('jupyt:cell-selected', handleCellSelected);
        };
    }, [value, onChange]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { component: "form", onSubmit: onSubmit, sx: {
            display: 'flex',
            gap: 1,
            p: 1,
            bgcolor: theme => theme.palette.mode === 'dark' ? 'background.paper' : 'grey.50',
            borderRadius: 2,
            border: '1px solid',
            borderColor: theme => theme.palette.mode === 'dark' ? 'grey.800' : 'grey.200'
        } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__["default"], { fullWidth: true, multiline: true, maxRows: 4, variant: "outlined", placeholder: "Ask Jupyt AI anything... Use @cell to reference cells and @search to find datasets", value: value, onChange: e => onChange(e.target.value), onKeyDown: e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    onSubmit(e);
                }
            }, disabled: isStreaming, inputRef: inputRef, sx: {
                '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                    bgcolor: theme => theme.palette.mode === 'dark' ? 'background.default' : 'white'
                }
            } }),
        isAgenticLooping ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { color: "error", onClick: onStopAgenticLoop, sx: {
                bgcolor: 'error.main',
                color: 'white',
                '&:hover': {
                    bgcolor: 'error.dark'
                }
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Stop__WEBPACK_IMPORTED_MODULE_4__["default"], null))) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { color: "primary", onClick: onSubmit, disabled: !value.trim() || isStreaming, sx: {
                bgcolor: 'primary.main',
                color: 'white',
                '&:hover': {
                    bgcolor: 'primary.dark'
                },
                '&.Mui-disabled': {
                    bgcolor: 'grey.300',
                    color: 'grey.500'
                }
            } }, isStreaming ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { size: 24, color: "inherit" })) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Send__WEBPACK_IMPORTED_MODULE_6__["default"], null))))));
}


/***/ }),

/***/ "./lib/components/chat-message.js":
/*!****************************************!*\
  !*** ./lib/components/chat-message.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ChatMessage: () => (/* binding */ ChatMessage)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Typography/Typography.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/IconButton/IconButton.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Button/Button.js");
/* harmony import */ var _mui_icons_material_ContentCopy__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/icons-material/ContentCopy */ "./node_modules/@mui/icons-material/esm/ContentCopy.js");
/* harmony import */ var _mui_icons_material_PlayArrow__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/icons-material/PlayArrow */ "./node_modules/@mui/icons-material/esm/PlayArrow.js");
/* harmony import */ var _mui_icons_material_Edit__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/icons-material/Edit */ "./node_modules/@mui/icons-material/esm/Edit.js");
/* harmony import */ var react_markdown__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! react-markdown */ "./node_modules/react-markdown/lib/index.js");
/* harmony import */ var _mui_material_CircularProgress__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/CircularProgress */ "./node_modules/@mui/material/esm/CircularProgress/CircularProgress.js");
/* harmony import */ var _mui_icons_material_Replay__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/icons-material/Replay */ "./node_modules/@mui/icons-material/esm/Replay.js");








function ChatMessage({ role, content, onCopyCode, onExecuteCode, onModifyCell, referencedCells = new Set(), operations, showNotification, onRevertOperation, canRevertOperation, notebookPanel }) {
    const isUser = role === 'user';
    const hasOperationWithCode = !!(operations === null || operations === void 0 ? void 0 : operations.some(op => op.code && op.code.trim()));
    console.log('operations', operations);
    const [revertStates, setRevertStates] = react__WEBPACK_IMPORTED_MODULE_0___default().useState({});
    const [canRevertFlags, setCanRevertFlags] = react__WEBPACK_IMPORTED_MODULE_0___default().useState({});
    react__WEBPACK_IMPORTED_MODULE_0___default().useEffect(() => {
        if (role === 'assistant' &&
            operations &&
            operations.length > 0 &&
            canRevertOperation) {
            const checkRevertStatus = async () => {
                const initialStates = {};
                const flags = {};
                operations.forEach((_, index) => {
                    initialStates[index] = 'checking';
                    flags[index] = false;
                });
                setRevertStates(initialStates);
                setCanRevertFlags(flags);
                for (let i = 0; i < operations.length; i++) {
                    const op = operations[i];
                    if (op.type !== 'delete_cell') {
                        const canRevert = await canRevertOperation(op);
                        setCanRevertFlags(prev => ({ ...prev, [i]: canRevert }));
                        setRevertStates(prev => ({ ...prev, [i]: 'idle' }));
                    }
                    else {
                        setRevertStates(prev => ({ ...prev, [i]: 'disabled' }));
                    }
                }
            };
            checkRevertStatus();
        }
    }, [operations, canRevertOperation, role]);
    const handleRevertClick = async (op, index) => {
        if (!onRevertOperation || !notebookPanel) {
            return;
        }
        setRevertStates(prev => ({ ...prev, [index]: 'reverting' }));
        const notebook = notebookPanel.content;
        let targetCell = undefined;
        if (op.type === 'update_cell' && typeof op.cell_index === 'number') {
            targetCell = notebook.widgets[op.cell_index];
        }
        else if (op.type === 'create_cell' && typeof op.cell_index === 'number') {
            targetCell = notebook.widgets[op.cell_index];
        }
        if (targetCell) {
            try {
                await onRevertOperation(op, targetCell);
                const canStillRevert = await (canRevertOperation === null || canRevertOperation === void 0 ? void 0 : canRevertOperation(op));
                setCanRevertFlags(prev => ({ ...prev, [index]: !!canStillRevert }));
                setRevertStates(prev => ({ ...prev, [index]: 'idle' }));
            }
            catch (e) {
                console.error('Revert failed:', e);
                showNotification === null || showNotification === void 0 ? void 0 : showNotification('Failed to revert operation.', 'error');
                setRevertStates(prev => ({ ...prev, [index]: 'idle' }));
            }
        }
        else {
            showNotification === null || showNotification === void 0 ? void 0 : showNotification('Could not find target cell to revert.', 'error');
            setRevertStates(prev => ({ ...prev, [index]: 'idle' }));
        }
    };
    const renderSpecialState = () => {
        if (content.includes('[Processing cell operation...]')) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { display: 'flex', alignItems: 'center', gap: 1, py: 2 } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_CircularProgress__WEBPACK_IMPORTED_MODULE_2__["default"], { size: 18, color: "info" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "body2", color: "text.secondary" }, "Processing cell operation...")));
        }
        if (content.includes('[Executing cell operation...]')) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { display: 'flex', alignItems: 'center', gap: 1, py: 2 } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_CircularProgress__WEBPACK_IMPORTED_MODULE_2__["default"], { size: 18, color: "primary" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "body2", color: "text.secondary" }, "Executing cell operation...")));
        }
        if (content.includes('[Cell operation executed]')) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { display: 'flex', alignItems: 'center', gap: 1, py: 2 } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "body2", color: "success.main" }, "Cell operation executed.")));
        }
        return null;
    };
    const cleanedContent = content;
    const renderCodeBlockFromMarkdown = (code) => {
        let cleanCode = code;
        // const langMatch = code.match(/^```(\w+)\n?/);
        if (cleanCode.startsWith('```')) {
            cleanCode = cleanCode.replace(/^```(\w+)?\n?/, '');
        }
        if (cleanCode.endsWith('```')) {
            cleanCode = cleanCode.replace(/```$/, '');
        }
        cleanCode = cleanCode.trim();
        if (!cleanCode) {
            return null;
        }
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                position: 'relative',
                my: 1,
                backgroundColor: 'action.hover',
                borderRadius: 1,
                overflow: 'hidden'
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("pre", { style: { margin: 0, position: 'relative' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", { style: {
                        display: 'block',
                        padding: '12px',
                        fontSize: '15px',
                        lineHeight: '1.6',
                        fontFamily: '"Fira Code", "Consolas", monospace',
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word'
                    } }, cleanCode)),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                    display: 'flex',
                    justifyContent: 'flex-end',
                    alignItems: 'center',
                    gap: 1,
                    p: 1,
                    borderTop: '1px solid',
                    borderColor: 'divider',
                    backgroundColor: 'background.paper'
                } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { size: "small", onClick: () => onCopyCode === null || onCopyCode === void 0 ? void 0 : onCopyCode(cleanCode), title: "Copy code" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_ContentCopy__WEBPACK_IMPORTED_MODULE_5__["default"], { fontSize: "small" })),
                onExecuteCode && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { size: "small", onClick: () => onExecuteCode(cleanCode), title: "Execute code in new cell" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_PlayArrow__WEBPACK_IMPORTED_MODULE_6__["default"], { fontSize: "small" }))),
                referencedCells.size > 0 && onModifyCell && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { display: 'flex', gap: 1 } }, Array.from(referencedCells).map(cellNumber => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { key: cellNumber, size: "small", onClick: () => onModifyCell(cleanCode, cellNumber - 1), title: `Modify cell ${cellNumber}`, sx: {
                        bgcolor: 'background.paper',
                        '&:hover': { bgcolor: 'grey.100' },
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                        position: 'relative'
                    } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Edit__WEBPACK_IMPORTED_MODULE_7__["default"], { fontSize: "small" }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { component: "span", sx: {
                            position: 'absolute',
                            top: -8,
                            right: -8,
                            fontSize: '0.75rem',
                            bgcolor: 'primary.main',
                            color: 'white',
                            width: 16,
                            height: 16,
                            borderRadius: '50%',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            lineHeight: '16px'
                        } }, cellNumber)))))))));
    };
    const markdownComponents = {
        code(props) {
            const { children, className, node, ...rest } = props;
            const match = /language-(\w+)/.exec(className || '');
            const isInline = !match && !(className === null || className === void 0 ? void 0 : className.startsWith('language-'));
            if (hasOperationWithCode && !isInline) {
                return null;
            }
            if (isInline) {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", { ...rest, style: {
                        backgroundColor: 'var(--jp-layout-color2, rgba(0,0,0,0.1))',
                        padding: '0.2em 0.4em',
                        margin: 0,
                        fontSize: '85%',
                        borderRadius: '3px',
                        fontFamily: 'monospace'
                    } }, children));
            }
            return renderCodeBlockFromMarkdown(String(children).trim());
        },
        p(props) {
            const content = react__WEBPACK_IMPORTED_MODULE_0___default().Children.toArray(props.children)
                .map(child => (typeof child === 'string' ? child : ''))
                .join('');
            if (content.trim() === '') {
                return null;
            }
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "body1", component: "p", sx: { mb: 1 } }, props.children));
        },
        ul(props) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { component: "ul", sx: { pl: 2, mb: 1 } }, props.children));
        },
        ol(props) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { component: "ol", sx: { pl: 2, mb: 1 } }, props.children));
        },
        li(props) {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { component: "li", sx: { mb: 0.5 } }, props.children));
        },
        pre({ children }) {
            const codeChild = react__WEBPACK_IMPORTED_MODULE_0___default().Children.toArray(children).find((child) => (child === null || child === void 0 ? void 0 : child.type) === 'code');
            return codeChild ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null, codeChild) : react__WEBPACK_IMPORTED_MODULE_0___default().createElement("pre", null, children);
        }
    };
    const renderIndividualOperation = (op, index) => {
        const cellDisplayIndex = typeof op.cell_index === 'number' ? op.cell_index + 1 : 'N/A';
        let title = '';
        let codeContent = op.code || '';
        switch (op.type) {
            case 'create_cell':
                title = `Create Cell (at index ${cellDisplayIndex})`;
                break;
            case 'update_cell':
                title = `Update Cell ${cellDisplayIndex}`;
                break;
            case 'delete_cell':
                title = `Delete Cell ${cellDisplayIndex}`;
                codeContent = `# Deleting cell ${cellDisplayIndex}`;
                break;
            default:
                title = `Unknown Operation on Cell ${cellDisplayIndex}`;
        }
        if (!codeContent.trim() && op.type !== 'delete_cell') {
            return null;
        }
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { key: `op-${index}`, sx: {
                my: 2,
                border: '1px solid',
                borderColor: 'divider',
                borderRadius: 1,
                overflow: 'hidden',
                backgroundColor: 'action.hover'
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { variant: "caption", sx: {
                    display: 'block',
                    p: 1,
                    backgroundColor: 'background.paper',
                    borderBottom: '1px solid',
                    borderColor: 'divider',
                    fontWeight: 'bold'
                } }, title),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("pre", { style: { margin: 0, position: 'relative' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", { style: {
                        display: 'block',
                        padding: '12px',
                        fontSize: '15px',
                        lineHeight: '1.6',
                        fontFamily: '"Fira Code", "Consolas", monospace',
                        whiteSpace: 'pre-wrap',
                        wordBreak: 'break-word'
                    } }, codeContent)),
            role === 'assistant' && canRevertFlags[index] && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                    p: 1,
                    borderTop: '1px solid',
                    borderColor: 'divider',
                    textAlign: 'right'
                } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { size: "small", variant: "outlined", color: "secondary", onClick: () => handleRevertClick(op, index), startIcon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Replay__WEBPACK_IMPORTED_MODULE_9__["default"], null), disabled: revertStates[index] === 'checking' ||
                        revertStates[index] === 'reverting' ||
                        revertStates[index] === 'disabled' }, revertStates[index] === 'reverting' ? 'Reverting...' : 'Revert')))));
    };
    const renderOperationBlocks = () => {
        if (!operations || operations.length === 0) {
            return null;
        }
        return operations.map(renderIndividualOperation);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
            display: 'flex',
            justifyContent: isUser ? 'flex-end' : 'flex-start',
            mb: 2,
            gap: 1
        } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                maxWidth: '85%',
                bgcolor: isUser ? 'primary.main' : 'background.paper',
                color: isUser ? 'primary.contrastText' : 'text.primary',
                borderRadius: 2,
                p: 2,
                boxShadow: theme => `0 1px 2px ${theme.palette.mode === 'dark' ? 'rgba(0,0,0,0.4)' : 'rgba(0,0,0,0.1)'}`
            } }, role === 'assistant' ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            renderSpecialState(),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: {
                    '& pre': {
                        position: 'relative',
                        bgcolor: theme => theme.palette.mode === 'dark' ? '#1E1E1E' : '#f5f5f5',
                        borderRadius: 1,
                        p: 2,
                        my: 2,
                        overflow: 'auto',
                        boxShadow: theme => `inset 0 0 8px ${theme.palette.mode === 'dark' ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.1)'}`,
                        border: theme => `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`
                    },
                    '& code': {
                        fontSize: '0.9rem',
                        fontFamily: '"Fira Code", "Consolas", monospace',
                        color: theme => theme.palette.mode === 'dark' ? '#D4D4D4' : '#333333',
                        lineHeight: '1.5'
                    },
                    '& p': {
                        m: 0,
                        color: 'text.primary',
                        '&:not(:last-child)': {
                            mb: 1.5
                        }
                    },
                    '& p > code': {
                        bgcolor: theme => theme.palette.mode === 'dark'
                            ? 'rgba(255,255,255,0.1)'
                            : 'rgba(0,0,0,0.1)',
                        color: 'text.primary',
                        px: 1,
                        py: 0.5,
                        borderRadius: 1,
                        fontFamily: '"Fira Code", "Consolas", monospace'
                    }
                } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_markdown__WEBPACK_IMPORTED_MODULE_10__.Markdown, { components: markdownComponents }, cleanedContent),
                renderOperationBlocks()))) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], null, cleanedContent)))));
}


/***/ }),

/***/ "./lib/components/chat.js":
/*!********************************!*\
  !*** ./lib/components/chat.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Chat: () => (/* binding */ Chat)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Button/Button.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../config */ "./lib/config.js");
/* harmony import */ var _chat_message__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./chat-message */ "./lib/components/chat-message.js");
/* harmony import */ var _chat_input__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./chat-input */ "./lib/components/chat-input.js");
/* harmony import */ var _chat_header__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./chat-header */ "./lib/components/chat-header.js");
/* harmony import */ var _services_cell_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../services/cell-service */ "./lib/services/cell-service.js");
/* harmony import */ var _utils_chatUtils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../utils/chatUtils */ "./lib/utils/chatUtils.js");
/* harmony import */ var _hooks_use_notebook_operations__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../hooks/use-notebook-operations */ "./lib/hooks/use-notebook-operations.js");
/* harmony import */ var _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../hooks/use-show-notification */ "./lib/hooks/use-show-notification.js");
/* harmony import */ var _hooks_use_agentic_loop_manager__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../hooks/use-agentic-loop-manager */ "./lib/hooks/use-agentic-loop-manager.js");
/* harmony import */ var _services_api_service__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../services/api-service */ "./lib/services/api-service.js");
/* harmony import */ var _utils_notebook_state_extractor__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../utils/notebook-state-extractor */ "./lib/utils/notebook-state-extractor.js");
/* harmony import */ var _hooks_use_agentic_state__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../hooks/use-agentic-state */ "./lib/hooks/use-agentic-state.js");
/* harmony import */ var _utils_cellOutputExtractor__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../utils/cellOutputExtractor */ "./lib/utils/cellOutputExtractor.js");
/* harmony import */ var _types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../types/cell-metadata */ "./lib/types/cell-metadata.js");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../plugins/cell-toolbar */ "./lib/plugins/cell-toolbar.js");
/* harmony import */ var _mui_icons_material_DoneAll__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @mui/icons-material/DoneAll */ "./node_modules/@mui/icons-material/esm/DoneAll.js");
/* harmony import */ var _mui_icons_material_ClearAll__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @mui/icons-material/ClearAll */ "./node_modules/@mui/icons-material/esm/ClearAll.js");





















function Chat({ notebookPanel, sessionContext }) {
    // Chat state
    const [messages, setMessages] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [input, setInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [isStreaming, setIsStreaming] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [currentType] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [sessionId, setSessionId] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(() => generateSessionId());
    const [hasPendingOperations, setHasPendingOperations] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    // Model configuration state
    const [modelConfig, setModelConfig] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)((0,_config__WEBPACK_IMPORTED_MODULE_2__.getModelConfig)());
    // Refs
    const messagesEndRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const cellServiceRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(_services_cell_service__WEBPACK_IMPORTED_MODULE_3__.CellService.getInstance());
    // Helper function to generate a random session ID
    function generateSessionId() {
        return `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    const scrollToBottom = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        var _a;
        (_a = messagesEndRef.current) === null || _a === void 0 ? void 0 : _a.scrollIntoView({ behavior: 'smooth' });
    }, []);
    // Handle model configuration change
    const handleModelConfigChange = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)((config) => {
        setModelConfig(config);
        (0,_config__WEBPACK_IMPORTED_MODULE_2__.saveModelConfig)(config);
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)(`Model updated to ${config.provider} - ${config.model}`, 'success');
    }, [_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (notebookPanel) {
            cellServiceRef.current.setNotebookPanel(notebookPanel);
        }
    }, [notebookPanel]);
    const { copyToNotebook, modifyCell, handleAddCell, handleDeleteCell, handleRevertOperation } = (0,_hooks_use_notebook_operations__WEBPACK_IMPORTED_MODULE_5__.useNotebookOperations)({
        notebookPanel,
        sessionContext,
        showNotification: _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification
    });
    // Cell operation executor for agentic loop
    const executeCellOperation = async (op) => {
        try {
            if (op.type === 'create_cell' &&
                op.code !== undefined &&
                op.cell_index !== undefined) {
                await handleAddCell(op.code, op.cell_index, !!op.run_needed);
                return undefined;
            }
            else if (op.type === 'update_cell' &&
                op.code !== undefined &&
                op.cell_index !== undefined) {
                await modifyCell(op.code, op.cell_index, !!op.run_needed);
                return undefined;
            }
            else if (op.type === 'delete_cell' && op.cell_index !== undefined) {
                await handleDeleteCell(op.cell_index);
                return undefined;
            }
        }
        catch (err) {
            (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)(`Cell operation failed: ${err instanceof Error ? err.message : 'Unknown error'}`, 'error');
            return `Error: ${err instanceof Error ? err.message : 'Unknown error'}`;
        }
        return undefined;
    };
    // Agentic state
    const { plan, setPlan, planStage, setPlanStage, cellOutput, setCellOutput } = (0,_hooks_use_agentic_state__WEBPACK_IMPORTED_MODULE_6__.useAgenticState)();
    // Agentic loop manager
    const { startAgenticLoop, cancelAgenticLoop, isLooping, revertAllChanges } = (0,_hooks_use_agentic_loop_manager__WEBPACK_IMPORTED_MODULE_7__.useAgenticLoopManager)({
        plan,
        setPlan,
        planStage,
        setPlanStage,
        cellOutput,
        setCellOutput,
        notebookPanel,
        sessionId,
        setMessages,
        onStreamingStateChange: setIsStreaming,
        executeCellOperation,
        extractTextOutputFromCell: _utils_cellOutputExtractor__WEBPACK_IMPORTED_MODULE_8__.extractTextOutputFromCell
    });
    // Conditional rendering for Revert All Changes button
    const shouldShowRevertButton = isLooping || !!plan;
    // Function to handle starting a new chat with a fresh session ID
    const handleNewChat = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        if (isStreaming || isLooping) {
            return; // Prevent starting new chat while streaming
        }
        // Reset states
        setMessages([]);
        setInput('');
        setSessionId(generateSessionId());
        // Reset agentic state if needed
        setPlan('');
        setPlanStage('');
        setCellOutput('');
        // Show notification
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)('Started new chat session', 'success');
        // Scroll to bottom
        setTimeout(() => scrollToBottom(), 100);
    }, [
        isStreaming,
        isLooping,
        setPlan,
        setPlanStage,
        setCellOutput,
        _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification,
        scrollToBottom
    ]);
    // Helper function to clean message content
    const cleanMessageContent = (content) => {
        // Correct the regex: Use single backslashes for bracket escaping in a regex literal
        const cleanedOfStatus = content
            .replace(/\n?\[COMPLETION_STATUS:[^\]]*\]/gi, '')
            .trim();
        // Remove cell operation tags separately
        return (0,_utils_chatUtils__WEBPACK_IMPORTED_MODULE_9__.removeCellOperationTags)(cleanedOfStatus);
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (notebookPanel) {
            cellServiceRef.current.setNotebookPanel(notebookPanel);
        }
    }, [notebookPanel]);
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim() || isStreaming || !notebookPanel) {
            return;
        }
        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [
            ...prev,
            {
                role: 'user',
                content: userMessage,
                timestamp: Date.now()
            }
        ]);
        setIsStreaming(true);
        const notebookState = (0,_utils_notebook_state_extractor__WEBPACK_IMPORTED_MODULE_10__.extractNotebookState)(notebookPanel);
        const includeSearch = userMessage.includes('@search');
        const payload = {
            query: userMessage,
            session_id: sessionId,
            notebook_state: notebookState,
            llm_config: modelConfig
        };
        if (includeSearch) {
            payload.search = true;
        }
        let assistantMsgIndex = -1;
        setMessages(prev => {
            assistantMsgIndex = prev.length;
            return [
                ...prev,
                {
                    role: 'assistant',
                    content: '',
                    timestamp: Date.now()
                }
            ];
        });
        scrollToBottom();
        let lastChunk = undefined;
        let fullContent = '';
        let initialCellOutput = null;
        try {
            for await (const chunk of (0,_services_api_service__WEBPACK_IMPORTED_MODULE_11__.streamAgenticAssistant)(payload)) {
                lastChunk = chunk;
                if (chunk.chunk_type !== 'end' && chunk.content) {
                    if (chunk.content.length > 0) {
                        fullContent += chunk.content;
                        setMessages(prev => {
                            // Update only the last assistant message
                            const updated = [...prev];
                            if (updated.length > 0 && updated[assistantMsgIndex]) {
                                updated[assistantMsgIndex] = {
                                    ...updated[assistantMsgIndex],
                                    // Clean the content as it streams
                                    content: cleanMessageContent(fullContent)
                                };
                            }
                            return updated;
                        });
                    }
                }
            }
        }
        catch (err) {
            setMessages(prev => {
                const updated = [...prev];
                if (updated.length > 0 && updated[assistantMsgIndex]) {
                    updated[assistantMsgIndex] = {
                        ...updated[assistantMsgIndex],
                        content: `Error: ${err instanceof Error ? err.message : 'Unknown error'}`
                    };
                }
                else {
                    // Add new error message if placeholder wasn't added correctly
                    updated.push({
                        role: 'assistant',
                        content: `Error: ${err instanceof Error ? err.message : 'Unknown error'}`,
                        timestamp: Date.now()
                    });
                }
                return updated;
            });
            setIsStreaming(false);
            return;
        }
        setIsStreaming(false);
        // Clean the final message content *before* potentially adding operations
        setMessages(prev => {
            const updated = [...prev];
            const lastMessageIndex = assistantMsgIndex; // Use the saved index
            if (lastMessageIndex >= 0 && updated[lastMessageIndex]) {
                updated[lastMessageIndex] = {
                    ...updated[lastMessageIndex],
                    content: cleanMessageContent(fullContent) // Clean the content here
                };
            }
            return updated;
        });
        // If agentic, execute all next_actions before entering the agentic loop
        let lastExecutedOperationIndex = -1;
        if (lastChunk &&
            lastChunk.next_action &&
            lastChunk.next_action.length > 0 &&
            lastChunk.completion_status === 'continue') {
            for (let i = 0; i < lastChunk.next_action.length; i++) {
                const op = lastChunk.next_action[i];
                await executeCellOperation(op);
                if (op.run_needed && typeof op.cell_index === 'number') {
                    lastExecutedOperationIndex = i; // Keep track of the last op that needs output checking
                }
            }
            // If the last executed operation needed running, wait for its output
            if (lastExecutedOperationIndex !== -1) {
                const op = lastChunk.next_action[lastExecutedOperationIndex];
                await new Promise(resolve => setTimeout(resolve, 100)); // Small delay
                await (async function waitForCellOutput() {
                    var _a, _b;
                    const pos = typeof op.cell_index === 'number' ? op.cell_index : 0;
                    const cell = (_b = (_a = notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.content) === null || _a === void 0 ? void 0 : _a.widgets) === null || _b === void 0 ? void 0 : _b[pos];
                    if (!cell) {
                        return;
                    }
                    const hasOutputs = (model) => {
                        return (model &&
                            typeof model === 'object' &&
                            'outputs' in model &&
                            model.outputs);
                    };
                    if (hasOutputs(cell.model)) {
                        let resolved = false;
                        const checkOutput = () => {
                            if (hasOutputs(cell.model)) {
                                const output = (0,_utils_cellOutputExtractor__WEBPACK_IMPORTED_MODULE_8__.extractTextOutputFromCell)(cell.model);
                                if (output && output.length > 0) {
                                    resolved = true;
                                    initialCellOutput = output;
                                }
                            }
                        };
                        const outputChanged = () => {
                            if (!resolved) {
                                checkOutput();
                            }
                        };
                        cell.model.outputs.changed.connect(outputChanged);
                        checkOutput();
                        setTimeout(() => {
                            if (!resolved) {
                                resolved = true;
                                cell.model.outputs.changed.disconnect(outputChanged);
                                initialCellOutput = (0,_utils_cellOutputExtractor__WEBPACK_IMPORTED_MODULE_8__.extractTextOutputFromCell)(cell.model);
                            }
                        }, 10000); // 10-second timeout
                    }
                })();
            }
        }
        // If agentic, enter the agentic loop
        if (lastChunk && lastChunk.completion_status === 'continue') {
            setCellOutput(initialCellOutput); // Set the initial cell output for the agentic loop
            await startAgenticLoop({
                query: userMessage,
                llmConfig: _config__WEBPACK_IMPORTED_MODULE_2__.DEFAULT_MODEL_CONFIG
            });
        }
        else if (lastChunk && lastChunk.chunk_type === 'end') {
            const operations = lastChunk.next_action;
            if (operations && operations.length > 0) {
                const notebook = notebookPanel.content;
                const model = notebookPanel.model;
                if (!model) {
                    (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)('Error: Notebook model not available.', 'error');
                    return;
                }
                for (const op of operations) {
                    const pendingMetadata = {
                        type: op.type,
                        code: op.code,
                        runNeeded: op.run_needed
                    };
                    try {
                        if (op.type === 'create_cell' &&
                            op.cell_index !== undefined &&
                            op.code !== undefined) {
                            // Insert a placeholder cell FIRST
                            model.sharedModel.insertCell(op.cell_index, {
                                cell_type: 'code',
                                source: ''
                            }); // Insert empty initially
                            const cellWidget = notebook.widgets[op.cell_index];
                            if (cellWidget) {
                                // Now set the metadata on the newly created cell
                                pendingMetadata.originalIndex = op.cell_index;
                                cellWidget.model.sharedModel.setMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY, pendingMetadata); // Cast to any
                                // Delay UI injection and selection slightly to allow DOM rendering
                                setTimeout(() => {
                                    var _a;
                                    // Add checks for safety and type narrowing
                                    if (cellWidget.isAttached &&
                                        cellWidget.node &&
                                        op.cell_index !== undefined) {
                                        (0,_plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_13__.injectOrUpdateCellUI)(cellWidget, notebookPanel);
                                        // Select the newly created cell to ensure UI updates
                                        notebook.activeCellIndex = op.cell_index; // Now type-safe
                                        notebook.scrollToCell(cellWidget);
                                    }
                                    else {
                                        console.warn(`Cell widget at index ${(_a = op.cell_index) !== null && _a !== void 0 ? _a : 'unknown'} not ready after delay for UI injection.`);
                                    }
                                }, 0);
                            }
                            else {
                                console.error(`Failed to get cell widget after creation at index ${op.cell_index}`);
                                (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)(`Error preparing cell creation at index ${op.cell_index + 1}.`, 'error');
                            }
                        }
                        else if (op.type === 'update_cell' &&
                            op.cell_index !== undefined &&
                            op.code !== undefined) {
                            const cellWidget = notebook.widgets[op.cell_index];
                            if (cellWidget) {
                                const oldCode = cellWidget.model.sharedModel.source;
                                pendingMetadata.oldCode = oldCode; // Store old code for diff
                                pendingMetadata.originalIndex = op.cell_index;
                                cellWidget.model.sharedModel.setMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY, pendingMetadata); // Cast to any
                                (0,_plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_13__.injectOrUpdateCellUI)(cellWidget, notebookPanel);
                            }
                            else {
                                (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)(`Error: Could not find cell ${op.cell_index + 1} to update.`, 'error');
                            }
                        }
                        else if (op.type === 'delete_cell' &&
                            op.cell_index !== undefined) {
                            const cellWidget = notebook.widgets[op.cell_index];
                            if (cellWidget) {
                                pendingMetadata.originalIndex = op.cell_index;
                                // For delete, just mark the cell for deletion via metadata
                                cellWidget.model.sharedModel.setMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY, pendingMetadata); // Cast to any
                                (0,_plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_13__.injectOrUpdateCellUI)(cellWidget, notebookPanel);
                            }
                            else {
                                (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)(`Error: Could not find cell ${op.cell_index + 1} to delete.`, 'error');
                            }
                        }
                    }
                    catch (metaError) {
                        console.error('Error setting metadata:', metaError);
                        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)(`Failed to set metadata for operation on cell ${op.cell_index !== undefined ? op.cell_index + 1 : 'N/A'}.`, 'error');
                    }
                }
                // Optionally, update the assistant message to indicate actions are pending cell approval
                setMessages(prev => {
                    const updated = [...prev];
                    // Ensure assistantMsgIndex is valid and the message exists
                    if (assistantMsgIndex >= 0 &&
                        assistantMsgIndex < updated.length &&
                        updated[assistantMsgIndex]) {
                        const currentContent = updated[assistantMsgIndex].content;
                        updated[assistantMsgIndex] = {
                            ...updated[assistantMsgIndex],
                            content: currentContent +
                                '\n\n*Code modifications suggested. Please approve or reject them in the notebook cells.*',
                            operations: operations // <-- Add the operations array here
                        };
                    }
                    else {
                        console.warn('Could not find assistant message to attach operations to. Index:', assistantMsgIndex);
                        // Optionally handle this case, maybe add a new message?
                    }
                    return updated;
                });
            }
        }
    };
    // --- NEW: Function to check if a specific operation can be reverted ---
    const checkCanRevert = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async (operation) => {
        if (!notebookPanel || typeof operation.cell_index !== 'number') {
            return false;
        }
        const notebook = notebookPanel.content;
        // For creates/updates, check the cell at the original index
        const cellWidget = notebook.widgets[operation.cell_index];
        if (cellWidget instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell && cellWidget.model) {
            const approvedMetadata = cellWidget.model.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.APPROVED_OPERATION_METADATA_KEY);
            // Can revert if approved metadata exists for this operation type
            return !!approvedMetadata && approvedMetadata.type === operation.type;
        }
        return false;
    }, [notebookPanel]);
    // --- NEW: Handler passed to ChatMessage to trigger revert ---
    const handleRevertRequest = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async (operation, cell) => {
        if (!cell.model) {
            return;
        }
        const model = cell.model;
        const approvedMetadata = model.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.APPROVED_OPERATION_METADATA_KEY);
        if (approvedMetadata && approvedMetadata.type === operation.type) {
            const success = await handleRevertOperation(cell, approvedMetadata);
            if (success) {
                // Clear the metadata AFTER successful revert
                model.sharedModel.deleteMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.APPROVED_OPERATION_METADATA_KEY);
                // Maybe add a confirmation message?
            }
            else {
                // handleRevertOperation already shows notification on failure
            }
        }
        else {
            (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)('Revert impossible: Cell state changed or metadata missing.', 'error');
        }
    }, [handleRevertOperation, _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification]);
    // Add function to check for pending operations
    const checkPendingOperations = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.content)) {
            return false;
        }
        const notebook = notebookPanel.content;
        for (const cell of notebook.widgets) {
            if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell && cell.model) {
                const pendingMetadata = cell.model.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY);
                if (pendingMetadata) {
                    return true;
                }
            }
        }
        return false;
    }, [notebookPanel]);
    // Update hasPendingOperations when notebook changes
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (!notebookPanel) {
            return;
        }
        const updatePendingStatus = () => {
            setHasPendingOperations(checkPendingOperations());
        };
        // Initial check
        updatePendingStatus();
        // Use MutationObserver to watch for metadata changes
        const observer = new MutationObserver(() => {
            updatePendingStatus();
        });
        // Observe the notebook for changes
        observer.observe(notebookPanel.node, {
            attributes: true,
            childList: true,
            subtree: true
        });
        return () => {
            observer.disconnect();
        };
    }, [notebookPanel, checkPendingOperations]);
    // Function to handle approve all
    const handleApproveAll = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async () => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.content)) {
            return;
        }
        const notebook = notebookPanel.content;
        // First, collect all cells with pending operations
        const pendingCells = notebook.widgets
            .map((cell, index) => ({ cell, index }))
            .filter(({ cell }) => {
            var _a;
            return cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell &&
                ((_a = cell.model) === null || _a === void 0 ? void 0 : _a.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY));
        });
        // Sort delete operations to the end to handle them last
        pendingCells.sort((a, b) => {
            var _a, _b;
            const aMetadata = (_a = a.cell.model) === null || _a === void 0 ? void 0 : _a.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY);
            const bMetadata = (_b = b.cell.model) === null || _b === void 0 ? void 0 : _b.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY);
            // Put delete operations at the end
            if (aMetadata.type === 'delete_cell' &&
                bMetadata.type !== 'delete_cell') {
                return 1;
            }
            if (bMetadata.type === 'delete_cell' &&
                aMetadata.type !== 'delete_cell') {
                return -1;
            }
            return 0;
        });
        // Process operations in order
        for (const { cell } of pendingCells) {
            if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell && cell.model) {
                const pendingMetadata = cell.model.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY);
                if (pendingMetadata) {
                    await (0,_plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_13__.handleApprove)(cell, notebookPanel, pendingMetadata);
                    // Add a small delay to allow the notebook to stabilize
                    await new Promise(resolve => setTimeout(resolve, 100));
                }
            }
        }
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)('All operations approved successfully', 'success');
    }, [notebookPanel, _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification]);
    // Function to handle reject all
    const handleRejectAll = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(async () => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.content)) {
            return;
        }
        const notebook = notebookPanel.content;
        for (const cell of notebook.widgets) {
            if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell && cell.model) {
                const pendingMetadata = cell.model.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_12__.PENDING_OPERATION_METADATA_KEY);
                if (pendingMetadata) {
                    await (0,_plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_13__.handleReject)(cell, notebookPanel, pendingMetadata);
                }
            }
        }
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification)('All operations rejected', 'success');
    }, [notebookPanel, _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_14__["default"], { sx: {
            display: 'flex',
            flexDirection: 'column',
            height: '100%',
            bgcolor: 'background.default',
            zIndex: 1000
        } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_14__["default"], { sx: {
                position: 'sticky',
                top: 0,
                zIndex: 1001,
                bgcolor: 'background.default',
                borderBottom: '1px solid',
                borderColor: 'divider',
                p: 2
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_chat_header__WEBPACK_IMPORTED_MODULE_15__.ChatHeader, { isStreaming: isStreaming, currentType: currentType, onNewChat: handleNewChat, onModelConfigChange: handleModelConfigChange })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_14__["default"], { sx: {
                flex: 1,
                overflow: 'auto',
                px: 3,
                py: 2
            } },
            messages.map((message, index) => {
                var _a;
                const { cellNumbers } = (0,_utils_chatUtils__WEBPACK_IMPORTED_MODULE_9__.extractCellReferences)(message.role === 'user'
                    ? message.content
                    : ((_a = messages[index - 1]) === null || _a === void 0 ? void 0 : _a.content) || '');
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_chat_message__WEBPACK_IMPORTED_MODULE_16__.ChatMessage, { key: index, role: message.role, content: message.content, onCopyCode: copyToNotebook, onExecuteCode: code => copyToNotebook(code, true), onModifyCell: modifyCell, onAddCell: handleAddCell, onDeleteCell: handleDeleteCell, referencedCells: cellNumbers, operations: message.operations, showNotification: _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_4__.showNotification, onRevertOperation: handleRevertRequest, canRevertOperation: checkCanRevert, notebookPanel: notebookPanel }));
            }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { ref: messagesEndRef })),
        shouldShowRevertButton && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_14__["default"], { sx: { display: 'flex', justifyContent: 'flex-end', mb: 1 } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_17__["default"], { variant: "outlined", color: "warning", onClick: async () => {
                    await revertAllChanges();
                } }, "Revert All Changes"))),
        hasPendingOperations && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_14__["default"], { sx: {
                position: 'fixed',
                bottom: 16,
                right: 16,
                display: 'flex',
                gap: 1,
                zIndex: 1002,
                bgcolor: 'background.paper',
                borderRadius: 1,
                boxShadow: 2,
                p: 1
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_17__["default"], { size: "small", variant: "contained", color: "primary", onClick: handleApproveAll, startIcon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_DoneAll__WEBPACK_IMPORTED_MODULE_18__["default"], null) }, "Approve All"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_17__["default"], { size: "small", variant: "outlined", color: "error", onClick: handleRejectAll, startIcon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_ClearAll__WEBPACK_IMPORTED_MODULE_19__["default"], null) }, "Reject All"))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_14__["default"], { sx: {
                p: 3,
                borderTop: '1px solid',
                borderColor: 'divider',
                bgcolor: 'background.default'
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_chat_input__WEBPACK_IMPORTED_MODULE_20__.ChatInput, { value: input, isStreaming: isStreaming || isLooping, onChange: setInput, onSubmit: handleSubmit, isAgenticLooping: isLooping, onStopAgenticLoop: cancelAgenticLoop }))));
}


/***/ }),

/***/ "./lib/components/jupyt-settings.js":
/*!******************************************!*\
  !*** ./lib/components/jupyt-settings.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Typography/Typography.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Paper/Paper.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/FormControl/FormControl.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/InputLabel/InputLabel.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Select/Select.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/MenuItem/MenuItem.js");
/* harmony import */ var _theme_provider__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../theme-provider */ "./lib/theme-provider.js");
/* harmony import */ var _model_selector__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./model-selector */ "./lib/components/model-selector.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../config */ "./lib/config.js");





/**
 * JupytSettings
 * Settings page for Jupyt AI. Contains model selection and appearance/theme settings.
 * User authentication has been moved to the UserProfile component.
 */
const JupytSettings = () => {
    const { themeMode, setThemeMode, currentTheme } = (0,_theme_provider__WEBPACK_IMPORTED_MODULE_1__.useTheme)();
    const [user, setUser] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    // Initialize user from storage
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const storedUser = (0,_config__WEBPACK_IMPORTED_MODULE_2__.getUserFromStorage)();
        if (storedUser) {
            setUser(storedUser);
        }
    }, []);
    // Handle theme change
    const handleThemeChange = (event) => {
        setThemeMode(event.target.value);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { p: 3, maxWidth: 600, margin: '0 auto' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "h4", sx: { mb: 2, fontWeight: 600 } }, "Jupyt Settings"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { sx: { p: 2, mb: 3 }, elevation: 2 },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "h6", sx: { mb: 1 } }, "Model Selection"),
            user ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_model_selector__WEBPACK_IMPORTED_MODULE_6__.ModelSelector, null)) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_7__["default"], { fullWidth: true, size: "small" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { id: "model-select-label" }, "Model"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { labelId: "model-select-label", label: "Model", value: "", disabled: true },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_10__["default"], { value: "" }, "(Login to select models)"))))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { sx: { p: 2 }, elevation: 2 },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "h6", sx: { mb: 1 } }, "Appearance & Theme"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_7__["default"], { fullWidth: true, size: "small" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { id: "theme-select-label" }, "Theme"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { labelId: "theme-select-label", label: "Theme", value: themeMode, onChange: handleThemeChange },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_10__["default"], { value: "light" }, "Light"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_10__["default"], { value: "dark" }, "Dark"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_10__["default"], { value: "system" },
                        "System (",
                        currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1),
                        ")"))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "body2", sx: { mt: 1, color: 'text.secondary' } },
                "Current theme:",
                ' ',
                currentTheme.charAt(0).toUpperCase() + currentTheme.slice(1)))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JupytSettings);


/***/ }),

/***/ "./lib/components/model-selector.js":
/*!******************************************!*\
  !*** ./lib/components/model-selector.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ModelSelector: () => (/* binding */ ModelSelector)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/CircularProgress/CircularProgress.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Typography/Typography.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/FormControl/FormControl.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/InputLabel/InputLabel.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Select/Select.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/MenuItem/MenuItem.js");
/* harmony import */ var _services_auth_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../services/auth-service */ "./lib/services/auth-service.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../config */ "./lib/config.js");




function ModelSelector({ onChange }) {
    const [availableModels, setAvailableModels] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({});
    const [allModels, setAllModels] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    const [error, setError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [modelConfig, setModelConfig] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)((0,_config__WEBPACK_IMPORTED_MODULE_1__.getModelConfig)());
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const fetchModels = async () => {
            setLoading(true);
            setError(null);
            try {
                const apiKey = (0,_config__WEBPACK_IMPORTED_MODULE_1__.getApiKey)();
                if (!apiKey) {
                    setError('API key not found. Please log in.');
                    setLoading(false);
                    return;
                }
                const authService = _services_auth_service__WEBPACK_IMPORTED_MODULE_2__.AuthService.getInstance();
                const response = await authService.getAvailableModels(apiKey);
                setAvailableModels(response.available_models);
                // Combine all models from different providers into a single array
                const combinedModels = [];
                Object.entries(response.available_models).forEach(([provider, models]) => {
                    models.forEach(model => {
                        combinedModels.push(model);
                    });
                });
                setAllModels(combinedModels);
            }
            catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to fetch models');
            }
            finally {
                setLoading(false);
            }
        };
        fetchModels();
    }, []);
    const handleModelChange = (event) => {
        const selectedModel = event.target.value;
        // Find which provider this model belongs to
        let selectedProvider = '';
        Object.entries(availableModels).forEach(([provider, models]) => {
            if (models.includes(selectedModel)) {
                selectedProvider = provider;
            }
        });
        const newConfig = {
            ...modelConfig,
            provider: selectedProvider,
            model: selectedModel
        };
        console.log('Selected model:', selectedModel);
        setModelConfig(newConfig);
        (0,_config__WEBPACK_IMPORTED_MODULE_1__.saveModelConfig)(newConfig);
        onChange === null || onChange === void 0 ? void 0 : onChange(newConfig);
    };
    if (loading) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: {
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                p: 2
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { size: 24, sx: { mr: 1 } }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "body2" }, "Loading models...")));
    }
    if (error) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { p: 2 } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { variant: "body2", color: "error" }, error)));
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', flexDirection: 'row', gap: 2, p: 2 } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_6__["default"], { fullWidth: true, size: "small" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_7__["default"], { id: "model-select-label" }, "Model"),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { labelId: "model-select-label", id: "model-select", value: modelConfig.model, label: "Model", onChange: handleModelChange }, allModels.map(model => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { key: model, value: model }, model)))))));
}


/***/ }),

/***/ "./lib/components/user-profile.js":
/*!****************************************!*\
  !*** ./lib/components/user-profile.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Typography/Typography.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Paper/Paper.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Alert/Alert.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/CircularProgress/CircularProgress.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/TextField/TextField.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Button/Button.js");
/* harmony import */ var _services_auth_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../services/auth-service */ "./lib/services/auth-service.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../config */ "./lib/config.js");




/**
 * UserProfile
 * Displays user profile information, including request usage and account details.
 * Allows login if not authenticated.
 */
const UserProfile = () => {
    // Authentication state
    const [user, setUser] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [userProfile, setUserProfile] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [authMode, setAuthMode] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('login');
    const [loginData, setLoginData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({
        username: '',
        password: ''
    });
    const [registerData, setRegisterData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({
        name: '',
        email: '',
        password: ''
    });
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [error, setError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    // Initialize user from storage and fetch profile data
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const storedUser = (0,_config__WEBPACK_IMPORTED_MODULE_1__.getUserFromStorage)();
        if (storedUser) {
            setUser(storedUser);
            fetchUserProfile();
        }
    }, []);
    // Fetch user profile data from API
    const fetchUserProfile = async () => {
        const apiKey = (0,_config__WEBPACK_IMPORTED_MODULE_1__.getApiKey)();
        if (!apiKey) {
            setError('No API key found. Please log in again.');
            return;
        }
        setLoading(true);
        try {
            const authService = _services_auth_service__WEBPACK_IMPORTED_MODULE_2__.AuthService.getInstance();
            console.log('Fetching user profile with API key length:', apiKey.length);
            console.log('API base URL:', authService.getBaseUrl());
            const profileData = await authService.getCurrentUser(apiKey);
            console.log('Profile data received:', profileData);
            setUserProfile(profileData);
            setLoading(false);
        }
        catch (err) {
            console.error('User profile fetch error:', err);
            let errorMessage = 'Failed to fetch user profile';
            if (err instanceof Error) {
                errorMessage = `${errorMessage}: ${err.message}`;
            }
            else if (typeof err === 'string') {
                errorMessage = err;
            }
            setError(errorMessage);
            setLoading(false);
        }
    };
    // Handle login
    const handleLogin = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            const authService = _services_auth_service__WEBPACK_IMPORTED_MODULE_2__.AuthService.getInstance();
            const response = await authService.login(loginData);
            // Create user object and save to storage
            const newUser = {
                user_id: '',
                name: '',
                email: loginData.username,
                api_key: response.api_key
            };
            // Save user to storage
            (0,_config__WEBPACK_IMPORTED_MODULE_1__.saveUserToStorage)(newUser);
            // Update local state
            setUser(newUser);
            setLoginData({ username: '', password: '' });
            // Fetch user profile
            await fetchUserProfile();
            setLoading(false);
        }
        catch (err) {
            setError(err instanceof Error ? err.message : 'Login failed');
            setLoading(false);
        }
    };
    // Handle register
    const handleRegister = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            const authService = _services_auth_service__WEBPACK_IMPORTED_MODULE_2__.AuthService.getInstance();
            const response = await authService.register(registerData);
            // Create user object
            const newUser = {
                user_id: response.user_id,
                name: registerData.name,
                email: registerData.email,
                api_key: response.api_key
            };
            // Save user to storage
            (0,_config__WEBPACK_IMPORTED_MODULE_1__.saveUserToStorage)(newUser);
            // Update local state
            setUser(newUser);
            setRegisterData({ name: '', email: '', password: '' });
            // Fetch user profile
            await fetchUserProfile();
            setLoading(false);
        }
        catch (err) {
            setError(err instanceof Error ? err.message : 'Registration failed');
            setLoading(false);
        }
    };
    // Handle logout
    const handleLogout = () => {
        (0,_config__WEBPACK_IMPORTED_MODULE_1__.clearUserData)();
        setUser(null);
        setUserProfile(null);
        setError(null);
    };
    // Handle form input changes
    const handleLoginChange = (e) => {
        const { name, value } = e.target;
        setLoginData(prev => ({ ...prev, [name]: value }));
    };
    const handleRegisterChange = (e) => {
        const { name, value } = e.target;
        setRegisterData(prev => ({ ...prev, [name]: value }));
    };
    // Switch between login and register forms
    const toggleAuthMode = () => {
        setAuthMode(prev => (prev === 'login' ? 'register' : 'login'));
        setError(null);
    };
    // Render usage bar
    const renderUsageBar = () => {
        if (!userProfile) {
            return null;
        }
        const usagePercentage = Math.min(Math.round((userProfile.request_count / userProfile.max_requests) * 100), 100);
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { mt: 2 } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', justifyContent: 'space-between', mb: 0.5 } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "body2", color: "text.secondary" }, "API Usage"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "body2", color: "text.secondary" },
                    userProfile.request_count,
                    " / ",
                    userProfile.max_requests,
                    " requests")),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: {
                    width: '100%',
                    height: 8,
                    bgcolor: 'grey.200',
                    borderRadius: 1,
                    overflow: 'hidden'
                } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: {
                        width: `${usagePercentage}%`,
                        height: '100%',
                        bgcolor: usagePercentage > 90 ? 'error.main' : 'primary.main',
                        transition: 'width 0.5s ease-in-out'
                    } }))));
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { p: 3, maxWidth: 600, margin: '0 auto' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "h4", sx: { mb: 2, fontWeight: 600 } }, "User Profile"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { sx: { p: 2 }, elevation: 2 },
            error && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_6__["default"], { severity: "error", sx: { mb: 2 } }, error)),
            loading && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', justifyContent: 'center', my: 3 } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_7__["default"], { size: 40 }))),
            user && userProfile && !loading ? (
            // Logged in user with profile data
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', flexDirection: 'column', gap: 2 } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "h6", gutterBottom: true }, "Account Information"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { label: "Email", variant: "outlined", size: "small", value: userProfile.email || user.email, disabled: true, fullWidth: true }),
                userProfile.name && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { label: "Name", variant: "outlined", size: "small", value: userProfile.name, disabled: true, fullWidth: true })),
                renderUsageBar(),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { variant: "outlined", color: "primary", onClick: handleLogout, disabled: loading, sx: { mt: 1 } }, "Logout"))) : user && !userProfile && !loading ? (
            // Logged in but no profile data yet
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', flexDirection: 'column', gap: 2 } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { variant: "body1" }, "Loading profile information..."),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { variant: "outlined", color: "primary", onClick: fetchUserProfile }, "Refresh Profile"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { variant: "outlined", color: "primary", onClick: handleLogout }, "Logout"))) : !loading ? (
            // Not logged in
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', flexDirection: 'column', gap: 2 } }, authMode === 'login' ? (
            // Login form
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: handleLogin },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { label: "Email", variant: "outlined", size: "small", fullWidth: true, margin: "normal", name: "username", type: "email", value: loginData.username, onChange: handleLoginChange, required: true, disabled: loading }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { label: "Password", variant: "outlined", size: "small", fullWidth: true, margin: "normal", name: "password", type: "password", value: loginData.password, onChange: handleLoginChange, required: true, disabled: loading }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', gap: 1, mt: 2 } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { variant: "contained", color: "primary", type: "submit", disabled: loading }, "Login"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { variant: "outlined", color: "primary", onClick: toggleAuthMode, disabled: loading }, "Sign Up Instead")))) : (
            // Register form
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", { onSubmit: handleRegister },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { label: "Name", variant: "outlined", size: "small", fullWidth: true, margin: "normal", name: "name", value: registerData.name, onChange: handleRegisterChange, required: true, disabled: loading }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { label: "Email", variant: "outlined", size: "small", fullWidth: true, margin: "normal", name: "email", type: "email", value: registerData.email, onChange: handleRegisterChange, required: true, disabled: loading }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_8__["default"], { label: "Password", variant: "outlined", size: "small", fullWidth: true, margin: "normal", name: "password", type: "password", value: registerData.password, onChange: handleRegisterChange, required: true, disabled: loading }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], { sx: { display: 'flex', gap: 1, mt: 2 } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { variant: "contained", color: "primary", type: "submit", disabled: loading }, "Sign Up"),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_9__["default"], { variant: "outlined", color: "primary", onClick: toggleAuthMode, disabled: loading }, "Login Instead")))))) : null)));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (UserProfile);


/***/ }),

/***/ "./lib/config.js":
/*!***********************!*\
  !*** ./lib/config.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   API_BASE_URL: () => (/* binding */ API_BASE_URL),
/* harmony export */   API_CONFIG: () => (/* binding */ API_CONFIG),
/* harmony export */   DEFAULT_MODEL_CONFIG: () => (/* binding */ DEFAULT_MODEL_CONFIG),
/* harmony export */   clearUserData: () => (/* binding */ clearUserData),
/* harmony export */   getApiKey: () => (/* binding */ getApiKey),
/* harmony export */   getModelConfig: () => (/* binding */ getModelConfig),
/* harmony export */   getUserFromStorage: () => (/* binding */ getUserFromStorage),
/* harmony export */   saveModelConfig: () => (/* binding */ saveModelConfig),
/* harmony export */   saveUserToStorage: () => (/* binding */ saveUserToStorage),
/* harmony export */   updateApiKey: () => (/* binding */ updateApiKey)
/* harmony export */ });
// Base URL for API
const API_BASE_URL = 'https://juno-242959672448.us-central1.run.app';
// Default API config without authentication
const API_CONFIG = {
    baseUrl: API_BASE_URL,
    apiKey: '' // Will be populated from user authentication
};
// Initialize API key from localStorage when module is loaded
(function initializeApiKey() {
    // Only run in browser environment with localStorage available
    if (typeof localStorage !== 'undefined') {
        const storedApiKey = localStorage.getItem('jupyt_api_key');
        if (storedApiKey) {
            API_CONFIG.apiKey = storedApiKey;
            console.log('API key loaded from storage');
        }
    }
})();
// Default model configuration
const DEFAULT_MODEL_CONFIG = {
    provider: 'openai',
    model: 'gpt-4.1',
    temperature: 0.2,
    stream: true
};
// Local storage keys
const USER_STORAGE_KEY = 'jupyt_user';
const API_KEY_STORAGE_KEY = 'jupyt_api_key';
const MODEL_CONFIG_STORAGE_KEY = 'jupyt_model_config';
// User state management
function saveUserToStorage(user) {
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    // Update API key in the config
    updateApiKey(user.api_key);
}
function getUserFromStorage() {
    const userJson = localStorage.getItem(USER_STORAGE_KEY);
    if (!userJson) {
        return null;
    }
    try {
        return JSON.parse(userJson);
    }
    catch (e) {
        console.error('Failed to parse user from storage', e);
        return null;
    }
}
function updateApiKey(apiKey) {
    localStorage.setItem(API_KEY_STORAGE_KEY, apiKey);
    API_CONFIG.apiKey = apiKey;
}
function getApiKey() {
    return localStorage.getItem(API_KEY_STORAGE_KEY);
}
function clearUserData() {
    localStorage.removeItem(USER_STORAGE_KEY);
    localStorage.removeItem(API_KEY_STORAGE_KEY);
    API_CONFIG.apiKey = '';
}
// Model configuration management
function saveModelConfig(config) {
    // Validate the model configuration before saving
    if (!config.model ||
        typeof config.model !== 'string' ||
        config.model.trim() === '') {
        console.warn('Attempted to save invalid model configuration');
        return;
    }
    // Ensure we're storing the exact model string as selected
    console.log('Saving model configuration:', config.model);
    localStorage.setItem(MODEL_CONFIG_STORAGE_KEY, JSON.stringify(config));
}
function getModelConfig() {
    const configJson = localStorage.getItem(MODEL_CONFIG_STORAGE_KEY);
    if (!configJson) {
        return DEFAULT_MODEL_CONFIG;
    }
    try {
        // Parse stored configuration and ensure model is valid
        const config = JSON.parse(configJson);
        // Verify that the model is a non-empty string
        if (!config.model ||
            typeof config.model !== 'string' ||
            config.model.trim() === '') {
            console.warn('Invalid model in stored config, using default model');
            return DEFAULT_MODEL_CONFIG;
        }
        return config;
    }
    catch (e) {
        console.error('Failed to parse model config from storage', e);
        return DEFAULT_MODEL_CONFIG;
    }
}


/***/ }),

/***/ "./lib/hooks/use-agentic-loop-manager.js":
/*!***********************************************!*\
  !*** ./lib/hooks/use-agentic-loop-manager.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   useAgenticLoopManager: () => (/* binding */ useAgenticLoopManager)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_notebook_state_extractor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../utils/notebook-state-extractor */ "./lib/utils/notebook-state-extractor.js");
/* harmony import */ var _services_api_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../services/api-service */ "./lib/services/api-service.js");
/* harmony import */ var _utils_chatUtils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/chatUtils */ "./lib/utils/chatUtils.js");




/**
 * React hook to manage the agentic loop for the Jupyt AI assistant.
 * Handles multi-step plans, cell execution, and streaming chat updates.
 * Ensures all streamed content for a single step is appended to a single chat bubble.
 */
function useAgenticLoopManager(args) {
    const isLoopingRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(false);
    const [isLooping, setIsLooping] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const initialNotebookStateRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    // Helper function to clean message content within the agentic loop
    const cleanAgenticContent = (content) => {
        // Replace [COMPLETION_STATUS:...] with a newline
        const cleanedOfStatus = content
            .replace(/\[COMPLETION_STATUS:[^\]]*\]/gi, '\n')
            .trim();
        // Remove <cell_operation> tags
        return (0,_utils_chatUtils__WEBPACK_IMPORTED_MODULE_1__.removeCellOperationTags)(cleanedOfStatus);
    };
    // Helper to wait for cell output with timeout
    async function waitForCellOutput(notebookPanel, cell_index, extractTextOutputFromCell, timeoutMs) {
        return new Promise(resolve => {
            var _a, _b;
            const cell = (_b = (_a = notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.content) === null || _a === void 0 ? void 0 : _a.widgets) === null || _b === void 0 ? void 0 : _b[cell_index];
            if (!cell) {
                return resolve('');
            }
            let resolved = false;
            const hasOutputs = (model) => {
                return (model &&
                    typeof model === 'object' &&
                    'outputs' in model &&
                    model.outputs);
            };
            const checkOutput = () => {
                if (hasOutputs(cell.model)) {
                    const output = extractTextOutputFromCell(cell.model);
                    if (output && output.length > 0) {
                        resolved = true;
                        resolve(output);
                    }
                }
            };
            // Listen for output changes
            const outputChanged = () => {
                if (!resolved) {
                    checkOutput();
                }
            };
            if (hasOutputs(cell.model)) {
                cell.model.outputs.changed.connect(outputChanged);
            }
            // Initial check
            checkOutput();
            // Timeout fallback
            setTimeout(() => {
                if (!resolved) {
                    resolved = true;
                    if (hasOutputs(cell.model)) {
                        cell.model.outputs.changed.disconnect(outputChanged);
                        resolve(extractTextOutputFromCell(cell.model));
                    }
                    else {
                        resolve('');
                    }
                }
            }, timeoutMs);
        });
    }
    const startAgenticLoop = async ({ query, llmConfig }) => {
        const { plan, setPlan, planStage, setPlanStage, cellOutput, setCellOutput, notebookPanel, sessionId, setMessages, onStreamingStateChange, executeCellOperation, extractTextOutputFromCell } = args;
        // Capture initial notebook state if panel exists
        if (notebookPanel) {
            try {
                initialNotebookStateRef.current = (0,_utils_notebook_state_extractor__WEBPACK_IMPORTED_MODULE_2__.extractNotebookState)(notebookPanel);
            }
            catch (e) {
                console.error('[AgenticLoop] Failed to extract initial notebook state:', e);
                initialNotebookStateRef.current = null; // Ensure it's null on error
            }
        }
        else {
            initialNotebookStateRef.current = null;
        }
        isLoopingRef.current = true;
        setIsLooping(true);
        let currentPlan = plan;
        let currentPlanStage = planStage;
        let currentCellOutput = cellOutput;
        let completionStatus = undefined;
        let first = true;
        while (isLoopingRef.current && (first || completionStatus === 'continue')) {
            first = false;
            const notebookState = (0,_utils_notebook_state_extractor__WEBPACK_IMPORTED_MODULE_2__.extractNotebookState)(notebookPanel);
            const payload = {
                query,
                session_id: sessionId,
                notebook_state: notebookState,
                llm_config: llmConfig,
                plan: currentPlan || undefined,
                plan_stage: currentPlanStage || undefined,
                cell_output: currentCellOutput || undefined
            };
            if (onStreamingStateChange) {
                onStreamingStateChange(true);
            }
            // Add a new assistant message and update its content as we stream
            let assistantMsgIndex = -1;
            setMessages(prev => {
                assistantMsgIndex = prev.length;
                return [
                    ...prev,
                    {
                        role: 'assistant',
                        content: '',
                        timestamp: Date.now()
                    }
                ];
            });
            let lastChunk = undefined;
            let fullContent = '';
            try {
                for await (const chunk of (0,_services_api_service__WEBPACK_IMPORTED_MODULE_3__.streamAgenticAssistant)(payload)) {
                    lastChunk = chunk;
                    if (chunk.chunk_type !== 'end' && chunk.content) {
                        fullContent += chunk.content;
                        setMessages(prev => {
                            const updated = [...prev];
                            if (updated.length > 0 && updated[assistantMsgIndex]) {
                                updated[assistantMsgIndex] = {
                                    ...updated[assistantMsgIndex],
                                    // Clean the content as it streams within the agentic loop
                                    content: cleanAgenticContent(fullContent)
                                };
                            }
                            return updated;
                        });
                    }
                }
            }
            catch (err) {
                setMessages(prev => [
                    ...prev,
                    {
                        role: 'assistant',
                        content: `Error: ${err instanceof Error ? err.message : 'Unknown error'}`,
                        timestamp: Date.now()
                    }
                ]);
                break;
            }
            finally {
                if (onStreamingStateChange) {
                    onStreamingStateChange(false);
                }
            }
            if (!lastChunk) {
                break;
            }
            // Print the end chunk for debugging
            console.log('[AgenticLoop] Received end chunk:', lastChunk);
            // Function to normalize operation types (internal helper)
            const normalizeOperation = (op) => {
                if (op.operation === 'update') {
                    return { ...op, type: 'update_cell' };
                }
                if (op.operation === 'create') {
                    return { ...op, type: 'create_cell' };
                }
                if (op.operation === 'delete') {
                    return { ...op, type: 'delete_cell' };
                }
                return op;
            };
            // Extract operations *before* potential execution
            const operations = lastChunk.next_action
                ? lastChunk.next_action.map(normalizeOperation)
                : [];
            // Update the final message content *and* add operations
            setMessages(prev => {
                const updated = [...prev];
                if (updated.length > 0 && updated[assistantMsgIndex]) {
                    updated[assistantMsgIndex] = {
                        ...updated[assistantMsgIndex],
                        content: cleanAgenticContent(fullContent),
                        operations: operations.length > 0 ? operations : undefined // Add operations
                    };
                }
                return updated;
            });
            // Extract plan, plan_stage, completion_status
            if (lastChunk.plan) {
                setPlan(lastChunk.plan);
            }
            if (lastChunk.plan_stage) {
                setPlanStage(lastChunk.plan_stage);
            }
            currentPlan = lastChunk.plan || currentPlan;
            currentPlanStage = lastChunk.plan_stage || currentPlanStage;
            completionStatus = lastChunk.completion_status || undefined;
            // Debug: Print next_action array
            if (lastChunk.next_action) {
                console.log('[AgenticLoop] next_action array:', lastChunk.next_action);
            }
            // If cell operations are required, execute them and get the output of the last one needing execution
            let output = '';
            let lastExecutedOperationIndex = -1; // Index of the last operation that required running
            if (operations && operations.length > 0) {
                // Use the extracted operations variable
                for (let i = 0; i < operations.length; i++) {
                    const op = operations[i]; // Use the extracted operations variable
                    await executeCellOperation(op);
                    if (op.run_needed && typeof op.cell_index === 'number') {
                        lastExecutedOperationIndex = i; // Track the last operation that needs output check
                    }
                }
                // Wait for the output of the *last* operation that needed to be run
                if (lastExecutedOperationIndex !== -1) {
                    const lastOpToRun = operations[lastExecutedOperationIndex];
                    // Ensure cell_index is valid before waiting
                    if (typeof lastOpToRun.cell_index === 'number') {
                        output = await waitForCellOutput(notebookPanel, lastOpToRun.cell_index, extractTextOutputFromCell, 10000);
                    }
                }
            }
            // If error output was explicitly provided in the chunk, use it (overwrites executed output)
            if (lastChunk.cell_output) {
                output = lastChunk.cell_output;
            }
            setCellOutput(output);
            currentCellOutput = output;
            setMessages(prev => {
                const updated = [...prev];
                if (updated.length > 0 && updated[assistantMsgIndex]) {
                    updated[assistantMsgIndex] = {
                        ...updated[assistantMsgIndex],
                        content: cleanAgenticContent(fullContent)
                    };
                }
                return updated;
            });
        }
        isLoopingRef.current = false;
        setIsLooping(false);
    };
    const cancelAgenticLoop = () => {
        isLoopingRef.current = false;
        setIsLooping(false);
    };
    const revertAllChanges = async () => {
        // stop the loop if it's running
        if (isLoopingRef.current) {
            cancelAgenticLoop();
        }
        if (!initialNotebookStateRef.current || !args.notebookPanel) {
            console.warn('[AgenticLoop] Cannot revert: initial state or notebook panel not available.');
            args.setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: 'Cannot revert: initial notebook state was not saved or panel is not available.',
                    timestamp: Date.now()
                }
            ]);
            return;
        }
        if (isLoopingRef.current) {
            cancelAgenticLoop(); // Stop any ongoing loop first
        }
        const { cells: initialCells } = initialNotebookStateRef.current;
        const currentNotebookPanel = args.notebookPanel;
        args.setMessages(prev => [
            ...prev,
            {
                role: 'assistant',
                content: 'Attempting to revert changes...',
                timestamp: Date.now()
            }
        ]);
        try {
            const model = currentNotebookPanel.content.model;
            if (!model) {
                console.error('[AgenticLoop] Revert failed: Notebook model not found.');
                args.setMessages(prev => {
                    const updated = [...prev];
                    if (updated.length > 0 &&
                        updated[updated.length - 1].content.startsWith('Attempting to revert')) {
                        updated[updated.length - 1].content =
                            'Revert failed: Notebook model not found.';
                    }
                    return updated;
                });
                return;
            }
            // Delete all current cells.
            // Iterating downwards ensures cell indices are stable during deletion.
            const currentNumCells = currentNotebookPanel.content.widgets.length; // Or model.cells.length
            for (let i = currentNumCells - 1; i >= 0; i--) {
                await args.executeCellOperation({ type: 'delete_cell', cell_index: i });
            }
            // Re-create cells from the initial state
            for (const initialCell of initialCells) {
                // The CellOperation type does not support specifying cell_type on creation.
                // Cells will be created with their original content in the 'code' field,
                // likely resulting in a default cell type (e.g., code cell).
                const createOp = {
                    type: 'create_cell',
                    code: initialCell.source // Use 'code' field for cell content
                    // run_needed: false, // Optional: set to true if cells should be run after creation
                };
                await args.executeCellOperation(createOp);
            }
            // Optionally, restore active cell (enhancement for later)
            // if (initialNotebookStateRef.current.active_cell_index !== null &&
            //     model.cells.length > initialNotebookStateRef.current.active_cell_index) {
            //   currentNotebookPanel.content.activeCellIndex = initialNotebookStateRef.current.active_cell_index;
            //   // Ensure the cell is visible/scrolled to if possible
            // }
            args.setPlan(null);
            args.setPlanStage(null);
            args.setCellOutput(null);
            console.log('[AgenticLoop] Changes reverted successfully.');
            args.setMessages(prev => {
                const updated = [...prev];
                if (updated.length > 0 &&
                    updated[updated.length - 1].content.startsWith('Attempting to revert')) {
                    updated[updated.length - 1].content =
                        'Changes reverted successfully.';
                }
                else {
                    // if the "Attempting" message was somehow overwritten or not there.
                    return [
                        ...prev,
                        {
                            role: 'assistant',
                            content: 'Changes reverted successfully.',
                            timestamp: Date.now()
                        }
                    ];
                }
                return updated;
            });
        }
        catch (error) {
            console.error('[AgenticLoop] Error during revert:', error);
            args.setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: `Failed to revert changes: ${error instanceof Error ? error.message : String(error)}`,
                    timestamp: Date.now()
                }
            ]);
        }
        finally {
            initialNotebookStateRef.current = null; // Clear the stored state after attempt
        }
    };
    return { startAgenticLoop, cancelAgenticLoop, isLooping, revertAllChanges };
}


/***/ }),

/***/ "./lib/hooks/use-agentic-state.js":
/*!****************************************!*\
  !*** ./lib/hooks/use-agentic-state.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   useAgenticState: () => (/* binding */ useAgenticState)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

function useAgenticState() {
    const [plan, setPlan] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [planStage, setPlanStage] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [cellOutput, setCellOutput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    return {
        plan,
        setPlan,
        planStage,
        setPlanStage,
        cellOutput,
        setCellOutput
    };
}


/***/ }),

/***/ "./lib/hooks/use-notebook-operations.js":
/*!**********************************************!*\
  !*** ./lib/hooks/use-notebook-operations.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   useNotebookOperations: () => (/* binding */ useNotebookOperations)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils_chatUtils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../utils/chatUtils */ "./lib/utils/chatUtils.js");


function useNotebookOperations({ notebookPanel, sessionContext, showNotification }) {
    // Copy code to a new cell and optionally execute
    const copyToNotebook = async (code, shouldExecute = false) => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.model) || !sessionContext) {
            showNotification('No notebook is open. Please open a notebook first.', 'error');
            return;
        }
        try {
            const notebook = notebookPanel.content;
            const model = notebookPanel.model;
            if (!model || !notebook || !notebook.model) {
                showNotification('Error: Could not access notebook content.', 'error');
                return;
            }
            const activeCellIndex = notebook.activeCellIndex;
            const newCellIndex = activeCellIndex + 1;
            model.sharedModel.insertCell(newCellIndex, {
                cell_type: 'code',
                source: (0,_utils_chatUtils__WEBPACK_IMPORTED_MODULE_1__.stripCodeBlockMarkers)(code),
                metadata: {},
                outputs: []
            });
            notebook.activeCellIndex = newCellIndex;
            if (shouldExecute) {
                await sessionContext.ready;
                await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.run(notebook, sessionContext);
            }
            const activeCell = notebook.activeCell;
            if (activeCell) {
                notebook.scrollToCell(activeCell);
            }
            showNotification(shouldExecute
                ? 'Code executed in notebook.'
                : 'Code copied to notebook.', 'success');
        }
        catch (error) {
            showNotification(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
        }
    };
    // Modify an existing cell
    const modifyCell = async (code, cell_index, run_needed) => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.model)) {
            showNotification('No notebook is open. Please open a notebook first.', 'error');
            return;
        }
        try {
            const notebook = notebookPanel.content;
            if (cell_index < 0 || cell_index >= notebook.widgets.length) {
                showNotification(`Invalid cell index ${cell_index + 1}`, 'error');
                return;
            }
            const cell = notebook.widgets[cell_index];
            const cleanCode = (0,_utils_chatUtils__WEBPACK_IMPORTED_MODULE_1__.stripCodeBlockMarkers)(code);
            cell.model.sharedModel.setSource(cleanCode);
            if (run_needed) {
                await (sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.ready);
                notebook.activeCellIndex = cell_index;
                await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.run(notebook, sessionContext);
            }
            showNotification(`Cell ${cell_index + 1} updated successfully${run_needed ? ' and executed' : ''}`, 'success');
        }
        catch (error) {
            showNotification(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
        }
    };
    // Add a new cell at a given position
    const handleAddCell = async (code, cell_index, run_needed) => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.model)) {
            showNotification('No notebook is open. Please open a notebook first.', 'error');
            return;
        }
        try {
            const notebook = notebookPanel.content;
            const model = notebookPanel.model;
            if (!model || !notebook || !notebook.model) {
                showNotification('Error: Could not access notebook content.', 'error');
                return;
            }
            if (cell_index < 0 || cell_index > notebook.widgets.length) {
                showNotification(`Invalid cell index ${cell_index + 1}`, 'error');
                return;
            }
            const cleanCode = (0,_utils_chatUtils__WEBPACK_IMPORTED_MODULE_1__.stripCodeBlockMarkers)(code);
            model.sharedModel.insertCell(cell_index, {
                cell_type: 'code',
                source: cleanCode,
                metadata: {},
                outputs: []
            });
            notebook.activeCellIndex = cell_index;
            if (run_needed) {
                await (sessionContext === null || sessionContext === void 0 ? void 0 : sessionContext.ready);
                await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.run(notebook, sessionContext);
            }
            const activeCell = notebook.activeCell;
            if (activeCell) {
                notebook.scrollToCell(activeCell);
            }
            showNotification(run_needed
                ? `Code executed at cell index ${cell_index + 1}.`
                : `Code added at cell index ${cell_index + 1}.`, 'success');
        }
        catch (error) {
            showNotification(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
        }
    };
    // Delete a cell at a given position
    const handleDeleteCell = async (cell_index) => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.model)) {
            showNotification('No notebook is open. Please open a notebook first.', 'error');
            return;
        }
        try {
            const notebook = notebookPanel.content;
            if (cell_index < 0 || cell_index >= notebook.widgets.length) {
                showNotification(`Invalid cell index ${cell_index + 1}`, 'error');
                return;
            }
            notebookPanel.model.sharedModel.deleteCell(cell_index);
            showNotification(`Cell at index ${cell_index + 1} deleted successfully`, 'success');
        }
        catch (error) {
            showNotification(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
        }
    };
    const handleRevertOperation = async (cell, metadata) => {
        if (!(notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.model) || !cell.model) {
            showNotification('Notebook or cell model not available for revert.', 'error');
            return false;
        }
        const notebook = notebookPanel.content;
        const notebookModel = notebookPanel.model;
        const cellModel = cell.model;
        console.log('Attempting revert:', metadata.type, 'for cell:', cellModel.id);
        try {
            switch (metadata.type) {
                case 'create_cell':
                    // eslint-disable-next-line no-case-declarations
                    const indexToDelete = notebook.widgets.findIndex(w => w === cell);
                    if (indexToDelete !== -1) {
                        notebookModel.sharedModel.deleteCell(indexToDelete);
                        showNotification('Cell creation reverted (cell deleted).', 'success');
                        return true; // Revert successful
                    }
                    else {
                        throw new Error('Could not find index for created cell to revert-delete.');
                    }
                // No return needed here due to throw/return above
                case 'update_cell':
                    if (metadata.previousCode !== undefined) {
                        cellModel.sharedModel.setSource(metadata.previousCode);
                        // TODO: Decide if running the cell after revert is desired/needed
                        showNotification('Cell update reverted.', 'success');
                        return true; // Revert successful
                    }
                    else {
                        throw new Error('Cannot revert update: Previous code not found in metadata.');
                    }
                // No return needed here due to throw/return above
                case 'delete_cell':
                    showNotification('Cannot revert a delete operation this way.', 'error');
                    console.warn('Attempted to revert a delete operation via handleRevertOperation');
                    return false; // Revert not possible/applicable
                default:
                    showNotification(`Cannot revert unsupported operation type: ${metadata.type}`, 'error');
                    return false; // Revert failed
            }
        }
        catch (error) {
            console.error('Error reverting operation:', error);
            showNotification(`Failed to revert operation: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
            return false; // Revert failed
        }
    };
    return {
        copyToNotebook,
        modifyCell,
        handleAddCell,
        handleDeleteCell,
        handleRevertOperation
    };
}


/***/ }),

/***/ "./lib/hooks/use-show-notification.js":
/*!********************************************!*\
  !*** ./lib/hooks/use-show-notification.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   showNotification: () => (/* binding */ showNotification)
/* harmony export */ });
const showNotification = (message, type) => {
    const notification = document.createElement('div');
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.backgroundColor =
        type === 'success' ? '#4caf50' : '#f44336';
    notification.style.color = 'white';
    notification.style.padding = '16px';
    notification.style.borderRadius = '4px';
    notification.style.zIndex = '1000';
    notification.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => {
        document.body.removeChild(notification);
    }, type === 'success' ? 3000 : 5000);
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CommandIDs: () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./plugins/cell-toolbar */ "./lib/plugins/cell-toolbar.js");
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./panel */ "./lib/panel.js");





// Create the chat icon
const chatIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon({
    name: 'jupyter-ai:chat',
    svgstr: `<svg xmlns="http://www.w3.org/2000/svg" width="16" viewBox="0 0 24 24">
      <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
    </svg>`
});
var CommandIDs;
(function (CommandIDs) {
    /**
     * Command to toggle AI Chat sidebar visibility.
     */
    CommandIDs.toggleAiChat = 'jupyter-ai:toggle-chat';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the jupyt extension.
 */
const plugin = {
    id: 'jupyt:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    activate: (app, palette, settings) => {
        console.log('JupyterLab extension jupyt is activated!');
        const panel = new _panel__WEBPACK_IMPORTED_MODULE_3__.JupytPanel(app);
        panel.id = 'jupyt-panel';
        panel.title.label = 'Jupyt';
        panel.title.icon = chatIcon;
        panel.title.closable = true;
        app.shell.add(panel, 'right');
        const command = 'jupyt:open';
        app.commands.addCommand(command, {
            label: 'Open Jupyt',
            execute: () => {
                app.shell.activateById(panel.id);
                return null;
            }
        });
        palette.addItem({ command, category: 'Jupyt' });
    }
};
const plugins = [plugin, _plugins_cell_toolbar__WEBPACK_IMPORTED_MODULE_4__["default"]];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/panel.js":
/*!**********************!*\
  !*** ./lib/panel.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JupytPanel: () => (/* binding */ JupytPanel)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_chat__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./components/chat */ "./lib/components/chat.js");
/* harmony import */ var _components_jupyt_settings__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/jupyt-settings */ "./lib/components/jupyt-settings.js");
/* harmony import */ var _components_user_profile__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./components/user-profile */ "./lib/components/user-profile.js");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/IconButton/IconButton.js");
/* harmony import */ var _mui_icons_material_Settings__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/icons-material/Settings */ "./node_modules/@mui/icons-material/esm/Settings.js");
/* harmony import */ var _mui_icons_material_AccountCircle__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @mui/icons-material/AccountCircle */ "./node_modules/@mui/icons-material/esm/AccountCircle.js");
/* harmony import */ var _theme_provider__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./theme-provider */ "./lib/theme-provider.js");










/**
 * JupytPanel
 * Main sidebar panel for Jupyt, now with tabs for Chat, Settings, and User Profile.
 */
class JupytPanel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(app) {
        super();
        this._onCurrentWidgetChanged = () => {
            this._updateNotebookPanel();
        };
        this.toggleSettings = () => {
            this.state = {
                ...this.state,
                showSettings: !this.state.showSettings,
                showProfile: false
            };
            this.update();
        };
        this.toggleProfile = () => {
            this.state = {
                ...this.state,
                showProfile: !this.state.showProfile,
                showSettings: false
            };
            this.update();
        };
        this.app = app;
        this.commands = app.commands;
        this.addClass('jp-JupytPanel');
        this.node.style.position = 'relative';
        this.node.style.zIndex = '1000';
        this.state = {
            showSettings: false,
            showProfile: false
        };
        this._updateNotebookPanel();
        const shell = this.app.shell;
        if (shell && shell.currentChanged) {
            shell.currentChanged.connect(this._onCurrentWidgetChanged, this);
        }
    }
    _updateNotebookPanel() {
        const shell = this.app.shell;
        if (!shell) {
            console.warn('Shell is not available');
            return;
        }
        const currentWidget = shell.currentWidget;
        let notebookPanel;
        if (currentWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel) {
            notebookPanel = currentWidget;
        }
        else {
            const widgets = shell.widgets('main') || [];
            for (const widget of widgets) {
                if (widget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel) {
                    notebookPanel = widget;
                    break;
                }
            }
        }
        const sessionContext = notebookPanel === null || notebookPanel === void 0 ? void 0 : notebookPanel.sessionContext;
        if (this._notebookPanel !== notebookPanel ||
            this._sessionContext !== sessionContext) {
            this._notebookPanel = notebookPanel;
            this._sessionContext = sessionContext;
            this.update();
        }
    }
    dispose() {
        const shell = this.app.shell;
        if (shell && shell.currentChanged) {
            shell.currentChanged.disconnect(this._onCurrentWidgetChanged, this);
        }
        super.dispose();
    }
    render() {
        const { showSettings, showProfile } = this.state;
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_theme_provider__WEBPACK_IMPORTED_MODULE_3__.ThemeProvider, { commands: this.commands },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { height: '100%', display: 'flex', flexDirection: 'column' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: {
                        display: 'flex',
                        justifyContent: 'flex-end',
                        alignItems: 'center',
                        padding: '4px 8px',
                        borderBottom: '1px solid var(--jp-border-color1)'
                    } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { onClick: this.toggleProfile, size: "small", title: "User Profile", sx: { mr: 1 } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_AccountCircle__WEBPACK_IMPORTED_MODULE_6__["default"], { fontSize: "small" })),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_5__["default"], { onClick: this.toggleSettings, size: "small", title: "Settings" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_Settings__WEBPACK_IMPORTED_MODULE_7__["default"], { fontSize: "small" }))),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_4__["default"], { sx: { flex: 1, overflow: 'auto', position: 'relative' } }, showSettings ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_jupyt_settings__WEBPACK_IMPORTED_MODULE_8__["default"], null)) : showProfile ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_user_profile__WEBPACK_IMPORTED_MODULE_9__["default"], null)) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_chat__WEBPACK_IMPORTED_MODULE_10__.Chat, { notebookPanel: this._notebookPanel, sessionContext: this._sessionContext }))))));
    }
}


/***/ }),

/***/ "./lib/plugins/cell-toolbar.js":
/*!*************************************!*\
  !*** ./lib/plugins/cell-toolbar.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   handleApprove: () => (/* binding */ handleApprove),
/* harmony export */   handleReject: () => (/* binding */ handleReject),
/* harmony export */   injectOrUpdateCellUI: () => (/* binding */ injectOrUpdateCellUI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _services_cell_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../services/cell-service */ "./lib/services/cell-service.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _components_cell_approval_controls__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../components/cell-approval-controls */ "./lib/components/cell-approval-controls.js");
/* harmony import */ var _types_cell_metadata__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../types/cell-metadata */ "./lib/types/cell-metadata.js");
/* harmony import */ var _hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../hooks/use-show-notification */ "./lib/hooks/use-show-notification.js");








const JUPYT_UI_CONTAINER_CLASS = 'jupyt-cell-ui-container';
/**
 * Injects or updates the Jupyt UI (Approval controls) in a cell based on metadata.
 */
const injectOrUpdateCellUI = (cell, panel) => {
    if (!cell.model ||
        !(cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell) ||
        !cell.inputArea /* Check needed for typing */) {
        return;
    }
    const model = cell.model;
    const pendingMetadata = model.sharedModel.getMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_4__.PENDING_OPERATION_METADATA_KEY);
    // Find container within the main cell node
    let container = cell.node.querySelector(`:scope > .${JUPYT_UI_CONTAINER_CLASS}`);
    // Clean up existing UI if no relevant metadata is found
    if (!pendingMetadata) {
        if (container) {
            react_dom__WEBPACK_IMPORTED_MODULE_3___default().unmountComponentAtNode(container);
            container.remove();
        }
        return;
    }
    // Create container if it doesn't exist
    if (!container) {
        container = document.createElement('div');
        container.className = JUPYT_UI_CONTAINER_CLASS;
        // Add margin below the container
        container.style.marginTop = '10px';
        // Add left margin to align with cell content
        container.style.marginLeft = '70px'; // Estimated prompt width
        // Append to the main cell node (instead of prepending)
        cell.node.appendChild(container);
    }
    // Render the approval component if pending metadata exists
    react_dom__WEBPACK_IMPORTED_MODULE_3___default().render(react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_components_cell_approval_controls__WEBPACK_IMPORTED_MODULE_5__.CellApprovalControls, {
        pendingOperation: pendingMetadata,
        onApprove: () => handleApprove(cell, panel, pendingMetadata),
        onReject: () => handleReject(cell, panel, pendingMetadata)
    }), container);
};
/**
 * Handles the approval of a pending operation.
 */
const handleApprove = async (cell, panel, metadata) => {
    var _a, _b;
    if (!cell.model) {
        return;
    }
    const model = cell.model;
    // --- IMMEDIATE UI REMOVAL ---
    // Clear pending metadata *first* to trigger UI removal immediately
    try {
        model.sharedModel.deleteMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_4__.PENDING_OPERATION_METADATA_KEY);
        injectOrUpdateCellUI(cell, panel);
    }
    catch (e) {
        console.error('Failed to clear pending metadata for UI removal:', e);
        // Continue with approval attempt anyway
    }
    // --- END IMMEDIATE UI REMOVAL ---
    const notebook = panel.content;
    const notebookModel = panel.model;
    if (!notebookModel) {
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Notebook model not found. Cannot approve.', 'error');
        // Attempt to clear approved metadata if it was somehow set before failure
        try {
            model.sharedModel.deleteMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_4__.APPROVED_OPERATION_METADATA_KEY);
        }
        catch (_c) {
            return;
        }
    }
    try {
        let approvedMetadata = null;
        let cellIndexToRun = null;
        const runAfterDelete = false;
        switch (metadata.type) {
            case 'create_cell':
                if (metadata.code !== undefined) {
                    model.sharedModel.setSource(metadata.code);
                    approvedMetadata = {
                        type: 'create_cell',
                        previousCodeForCreate: '',
                        runAfterApproval: metadata.runNeeded
                    };
                    const index = notebook.widgets.findIndex(w => w === cell);
                    if (index !== -1 && metadata.runNeeded) {
                        cellIndexToRun = index;
                    }
                    (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Cell created successfully.', 'success');
                }
                else {
                    throw new Error('Missing code for create operation.');
                }
                break;
            case 'update_cell':
                if (metadata.code !== undefined && metadata.oldCode !== undefined) {
                    model.sharedModel.setSource(metadata.code);
                    approvedMetadata = {
                        type: 'update_cell',
                        previousCode: metadata.oldCode,
                        runAfterApproval: metadata.runNeeded
                    };
                    const index = notebook.widgets.findIndex(w => w === cell);
                    if (index !== -1 && metadata.runNeeded) {
                        cellIndexToRun = index;
                    }
                    (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Cell updated successfully.', 'success');
                }
                else {
                    throw new Error('Missing code or oldCode for update operation.');
                }
                break;
            case 'delete_cell':
                // eslint-disable-next-line no-case-declarations
                const indexToDelete = notebook.widgets.findIndex(w => w === cell);
                if (indexToDelete !== -1) {
                    // Store the next cell index before deletion if we need to run it
                    let nextCellIndex = null;
                    if (metadata.runNeeded &&
                        indexToDelete + 1 < notebook.widgets.length) {
                        nextCellIndex = indexToDelete + 1;
                    }
                    // Delete the cell
                    if (notebookModel) {
                        notebookModel.sharedModel.deleteCell(indexToDelete);
                        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Cell deleted successfully.', 'success');
                        // If we need to run the next cell after deletion
                        if (nextCellIndex !== null &&
                            ((_a = panel.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel)) {
                            notebook.activeCellIndex = nextCellIndex;
                            await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.run(notebook, panel.sessionContext);
                        }
                    }
                    else {
                        throw new Error('Could not find cell index to delete.');
                    }
                }
                break;
            default:
                console.warn('Unsupported operation type for approval:', metadata.type);
                (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)(`Unsupported operation: ${metadata.type}`, 'error');
                return;
        }
        // Set approved metadata *after* operation succeeds (if applicable)
        if (approvedMetadata) {
            // We already deleted pending, just set approved
            model.sharedModel.setMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_4__.APPROVED_OPERATION_METADATA_KEY, approvedMetadata);
        }
        // For delete, the metadata is gone with the cell.
        // Run Cell if Needed
        if (cellIndexToRun !== null && ((_b = panel.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel)) {
            notebook.activeCellIndex = cellIndexToRun;
            await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.run(notebook, panel.sessionContext);
        }
        else if (runAfterDelete) {
            console.log('Run needed after delete - current implementation does not run.');
        }
    }
    catch (error) {
        console.error('Error approving operation:', error);
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)(`Failed to approve operation: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
        // Pending metadata was already cleared. Ensure approved isn't set if it failed.
        try {
            model.sharedModel.deleteMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_4__.APPROVED_OPERATION_METADATA_KEY);
        }
        catch (_d) {
            return;
        }
    }
};
/**
 * Handles the rejection of a pending operation.
 */
const handleReject = (cell, panel, metadata) => {
    if (!cell.model) {
        return;
    }
    const model = cell.model;
    // --- IMMEDIATE UI REMOVAL ---
    // Clear pending metadata *first* to trigger UI removal immediately
    try {
        model.sharedModel.deleteMetadata(_types_cell_metadata__WEBPACK_IMPORTED_MODULE_4__.PENDING_OPERATION_METADATA_KEY);
        injectOrUpdateCellUI(cell, panel);
    }
    catch (e) {
        console.error('Failed to clear pending metadata for UI removal:', e);
        // Continue with rejection attempt anyway
    }
    // --- END IMMEDIATE UI REMOVAL ---
    const notebook = panel.content;
    const notebookModel = panel.model;
    if (!notebookModel) {
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Notebook model not found. Cannot reject.', 'error');
        return;
    }
    try {
        switch (metadata.type) {
            case 'create_cell':
                // eslint-disable-next-line no-case-declarations
                const indexToDelete = notebook.widgets.findIndex(w => w === cell);
                if (indexToDelete !== -1) {
                    notebookModel.sharedModel.deleteCell(indexToDelete);
                    (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Cell creation rejected and placeholder removed.', 'success');
                }
                else {
                    throw new Error('Could not find index for rejected placeholder cell.');
                }
                return; // Exit after deletion
            case 'update_cell':
                (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Cell update rejected.', 'success');
                break; // Metadata already cleared
            case 'delete_cell':
                (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)('Cell deletion rejected.', 'success');
                break; // Metadata already cleared
            default:
                console.warn('Unsupported operation type for rejection:', metadata.type);
                (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)(`Cannot reject unsupported operation: ${metadata.type}`, 'error');
                return;
        }
        // Metadata was cleared at the start
    }
    catch (error) {
        console.error('Error rejecting operation:', error);
        (0,_hooks_use_show_notification__WEBPACK_IMPORTED_MODULE_6__.showNotification)(`Failed to reject operation: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
        // Metadata was already attempted to be cleared
    }
};
// --- Plugin Definition ---
const plugin = {
    id: 'jupyt:cell-toolbar',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebooks) => {
        const cellService = _services_cell_service__WEBPACK_IMPORTED_MODULE_7__.CellService.getInstance();
        notebooks.widgetAdded.connect((sender, panel) => {
            var _a, _b;
            const addAIButton = (cell) => {
                // Find the JupyterLab toolbar
                const jupyterToolbar = cell.node.querySelector('.jp-Toolbar');
                if (!jupyterToolbar) {
                    return;
                }
                // Remove any existing AI buttons to prevent duplicates
                const existingButtons = jupyterToolbar.querySelectorAll('.jupyt-ai-button');
                existingButtons.forEach(button => button.remove());
                // Add cell number label
                let cellNumberLabel = jupyterToolbar.querySelector('.jupyt-cell-number');
                if (!cellNumberLabel) {
                    cellNumberLabel = document.createElement('div');
                    cellNumberLabel.className = 'jupyt-cell-number';
                    cellNumberLabel.style.marginLeft = 'auto'; // Push to the right
                    cellNumberLabel.style.marginRight = '8px';
                    cellNumberLabel.style.fontSize = '12px';
                    cellNumberLabel.style.color =
                        'var(--jp-ui-font-color2)';
                    cellNumberLabel.style.fontFamily =
                        'var(--jp-ui-font-family)';
                    jupyterToolbar.appendChild(cellNumberLabel);
                }
                // Get cell index and update the label
                const notebook = panel.content;
                const cellIndex = notebook.widgets.findIndex(c => c === cell);
                if (cellNumberLabel) {
                    cellNumberLabel.textContent = `Cell [${cellIndex + 1}]`;
                }
                const button = document.createElement('button');
                button.className = 'jp-Button jp-ToolbarButton jupyt-ai-button';
                button.title = 'Use Jupyt Assistant for this cell';
                button.innerHTML = `
          <span class="jp-ToolbarButton-icon">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 0C3.6 0 0 3.6 0 8C0 12.4 3.6 16 8 16C12.4 16 16 12.4 16 8C16 3.6 12.4 0 8 0ZM8 14C4.7 14 2 11.3 2 8C2 4.7 4.7 2 8 2C11.3 2 14 4.7 14 8C14 11.3 11.3 14 8 14Z" fill="currentColor"/>
              <path d="M8 4C6.3 4 5 5.3 5 7C5 8.7 6.3 10 8 10C9.7 10 11 8.7 11 7C11 5.3 9.7 4 8 4ZM8 8C7.4 8 7 7.6 7 7C7 6.4 7.4 6 8 6C8.6 6 9 6.4 9 7C9 7.6 8.6 8 8 8Z" fill="currentColor"/>
            </svg>
          </span>
          <span class="jp-ToolbarButton-label">AI</span>
        `;
                button.onclick = () => {
                    cellService.selectCell(cell);
                };
                // Find the move up button (which is typically the first button)
                const moveUpButton = jupyterToolbar.querySelector('.jp-Button[data-command="notebook:move-cell-up"]');
                if (moveUpButton) {
                    // Insert after the move up button
                    moveUpButton.insertAdjacentElement('afterend', button);
                }
                else {
                    // Fallback: insert at the beginning of the toolbar
                    const firstButton = jupyterToolbar.querySelector('.jp-Button');
                    if (firstButton) {
                        firstButton.insertAdjacentElement('beforebegin', button);
                    }
                    else {
                        jupyterToolbar.insertBefore(button, jupyterToolbar.firstChild);
                    }
                }
            };
            // Function to update all cell numbers
            const updateAllCellNumbers = () => {
                panel.content.widgets.forEach((cell, index) => {
                    const toolbar = cell.node.querySelector('.jp-Toolbar');
                    if (toolbar) {
                        let numberLabel = toolbar.querySelector('.jupyt-cell-number');
                        if (!numberLabel) {
                            numberLabel = document.createElement('div');
                            numberLabel.className = 'jupyt-cell-number';
                            numberLabel.style.marginLeft = 'auto';
                            numberLabel.style.marginRight = '8px';
                            numberLabel.style.fontSize = '12px';
                            numberLabel.style.color =
                                'var(--jp-ui-font-color2)';
                            numberLabel.style.fontFamily =
                                'var(--jp-ui-font-family)';
                            toolbar.appendChild(numberLabel);
                        }
                        numberLabel.textContent = `Cell [${index + 1}]`;
                    }
                });
            };
            // --- NEW: Inject UI based on metadata for all cells ---
            const setupCellUIs = () => {
                panel.content.widgets.forEach(cell => {
                    if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell) {
                        injectOrUpdateCellUI(cell, panel);
                    }
                });
            };
            // Listen for metadata changes on ANY cell in the model
            (_a = panel.model) === null || _a === void 0 ? void 0 : _a.sharedModel.changed.connect((sharedModel, changes) => {
                if (changes.metadataChange) {
                    // Add a minimal delay to allow DOM updates before checking/injecting UI
                    setTimeout(() => {
                        setupCellUIs();
                    }, 50); // 50ms delay, adjust if needed
                }
            });
            // Listen for cell list changes (add/remove)
            (_b = panel.model) === null || _b === void 0 ? void 0 : _b.cells.changed.connect(() => {
                // No timeout - run immediately (might cause flicker if DOM isn't ready, but let's try)
                updateAllCellNumbers();
                setupCellUIs();
                // Potential TODO: Check if a slight delay is needed here if UI doesn't appear reliably
            });
            // Initial setup for existing cells
            panel.revealed.then(() => {
                // Keep this delay - needed to ensure initial DOM is ready
                setTimeout(() => {
                    panel.content.widgets.forEach(addAIButton);
                    updateAllCellNumbers();
                    setupCellUIs();
                }, 1000);
            });
            // Update AI button and UI on active cell change
            panel.content.activeCellChanged.connect((_, cell) => {
                if (cell) {
                    // No timeout - run immediately
                    addAIButton(cell);
                    if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_1__.CodeCell) {
                        injectOrUpdateCellUI(cell, panel);
                    }
                }
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/services/api-service.js":
/*!*************************************!*\
  !*** ./lib/services/api-service.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   streamAgenticAssistant: () => (/* binding */ streamAgenticAssistant)
/* harmony export */ });
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../config */ "./lib/config.js");

/**
 * Calls the /assistant endpoint and yields StreamChunk objects as they arrive.
 */
async function* streamAgenticAssistant(payload) {
    var _a;
    // Use the API key that was set during authentication
    const headers = {
        'Content-Type': 'application/json',
        'X-API-Key': _config__WEBPACK_IMPORTED_MODULE_0__.API_CONFIG.apiKey,
        Accept: 'text/event-stream'
    };
    // Validate API key exists
    if (!_config__WEBPACK_IMPORTED_MODULE_0__.API_CONFIG.apiKey) {
        throw new Error('API key is missing. Please log in first.');
    }
    else {
        // Log that we have a valid API key - this helps confirm it's loaded correctly after refresh
        console.log('Using API key from config (length):', _config__WEBPACK_IMPORTED_MODULE_0__.API_CONFIG.apiKey.length);
    }
    // Log the model being used for debugging
    console.log('Sending request with model:', payload);
    // Ensure the model is being sent in the correct format
    // The API expects the model to be passed as is, e.g. 'claude-3-7-sonnet'
    // No modifications are made to the model name selected by the user
    const response = await fetch(`${_config__WEBPACK_IMPORTED_MODULE_0__.API_CONFIG.baseUrl}/assistant`, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
    });
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    const reader = (_a = response.body) === null || _a === void 0 ? void 0 : _a.getReader();
    if (!reader) {
        throw new Error('Response body reader could not be created');
    }
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            break;
        }
        const chunkStr = decoder.decode(value, { stream: true });
        buffer += chunkStr;
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
            if (!line.startsWith('data:')) {
                continue;
            }
            const data = line.slice(5).trim();
            if (!data) {
                continue;
            }
            try {
                const chunk = JSON.parse(data);
                yield chunk;
            }
            catch (err) {
                // Ignore parse errors for incomplete lines
            }
        }
    }
}


/***/ }),

/***/ "./lib/services/auth-service.js":
/*!**************************************!*\
  !*** ./lib/services/auth-service.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   AuthService: () => (/* binding */ AuthService)
/* harmony export */ });
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../config */ "./lib/config.js");

class AuthService {
    constructor() {
        this.baseUrl = _config__WEBPACK_IMPORTED_MODULE_0__.API_CONFIG.baseUrl;
    }
    static getInstance() {
        if (!AuthService.instance) {
            AuthService.instance = new AuthService();
        }
        return AuthService.instance;
    }
    /**
     * Get the base URL used for API requests
     */
    getBaseUrl() {
        return this.baseUrl;
    }
    /**
     * Register a new user
     */
    async register(userData) {
        const response = await fetch(`${this.baseUrl}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Registration failed: ${response.status}`);
        }
        return await response.json();
    }
    /**
     * Login a user and get access token
     */
    async login(credentials) {
        const formData = new URLSearchParams();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);
        const response = await fetch(`${this.baseUrl}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Login failed: ${response.status}`);
        }
        return await response.json();
    }
    /**
     * Get available models
     */
    async getAvailableModels(apiKey) {
        const response = await fetch(`${this.baseUrl}/models`, {
            method: 'GET',
            headers: {
                'X-API-Key': apiKey
            }
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Failed to fetch models: ${response.status}`);
        }
        return await response.json();
    }
    /**
     * Get current user's profile information
     */
    async getCurrentUser(apiKey) {
        const response = await fetch(`${this.baseUrl}/users/me`, {
            method: 'GET',
            headers: {
                'X-API-Key': apiKey
            }
        });
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Failed to fetch user profile: ${response.status}`);
        }
        return await response.json();
    }
}


/***/ }),

/***/ "./lib/services/cell-service.js":
/*!**************************************!*\
  !*** ./lib/services/cell-service.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CellService: () => (/* binding */ CellService)
/* harmony export */ });
class CellService {
    constructor() {
        this.selectedCell = null;
        this.notebookPanel = null;
    }
    static getInstance() {
        if (!CellService.instance) {
            CellService.instance = new CellService();
        }
        return CellService.instance;
    }
    setNotebookPanel(panel) {
        this.notebookPanel = panel;
    }
    selectCell(cell) {
        this.selectedCell = cell;
        this.notifyCellSelected();
    }
    getCellNumber(cell) {
        if (!this.notebookPanel) {
            return -1;
        }
        return this.notebookPanel.content.widgets.indexOf(cell) + 1;
    }
    getCellByNumber(cellNumber) {
        if (!this.notebookPanel) {
            return null;
        }
        const index = cellNumber - 1;
        if (index >= 0 && index < this.notebookPanel.content.widgets.length) {
            return this.notebookPanel.content.widgets[index];
        }
        return null;
    }
    getCellById(cellId) {
        if (!this.notebookPanel) {
            return null;
        }
        const cells = this.notebookPanel.content.widgets;
        return cells.find(cell => cell.model.id === cellId) || null;
    }
    getCellInfo(cell) {
        return {
            id: cell.model.id,
            type: cell.model.type,
            content: cell.model.sharedModel.source,
            metadata: cell.model.metadata,
            cellNumber: this.getCellNumber(cell)
        };
    }
    updateCell(cellId, content) {
        if (!this.notebookPanel) {
            return;
        }
        const cells = this.notebookPanel.content.widgets;
        const cell = cells.find(c => c.model.id === cellId);
        if (cell) {
            cell.model.sharedModel.source = content;
        }
    }
    deleteCell(cellId) {
        if (!this.notebookPanel) {
            return;
        }
        const cells = this.notebookPanel.content.widgets;
        const cellIndex = cells.findIndex(c => c.model.id === cellId);
        if (cellIndex !== -1) {
            // this.notebookPanel.content.model?.cells.delete(cellIndex);
        }
    }
    notifyCellSelected() {
        if (this.selectedCell) {
            const cellInfo = this.getCellInfo(this.selectedCell);
            // Dispatch custom event for sidebar to listen
            const event = new CustomEvent('jupyt:cell-selected', {
                detail: cellInfo
            });
            document.dispatchEvent(event);
        }
    }
}


/***/ }),

/***/ "./lib/theme-provider.js":
/*!*******************************!*\
  !*** ./lib/theme-provider.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ThemeProvider: () => (/* binding */ ThemeProvider),
/* harmony export */   useTheme: () => (/* binding */ useTheme)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_styles__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/styles */ "./node_modules/@mui/material/esm/styles/ThemeProvider.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material */ "./node_modules/@mui/material/esm/CssBaseline/CssBaseline.js");
/* harmony import */ var _theme__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./theme */ "./lib/theme.js");




// Define known JupyterLab theme names
const JUPYTERLAB_LIGHT_THEME = 'JupyterLab Light';
const JUPYTERLAB_DARK_THEME = 'JupyterLab Dark';
// Create context with default values
const ThemeContext = (0,react__WEBPACK_IMPORTED_MODULE_0__.createContext)({
    themeMode: 'system',
    setThemeMode: () => { },
    currentTheme: 'light'
});
// Hook to use the theme context
const useTheme = () => (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(ThemeContext);
// Function to get JupyterLab's theme
const getJupyterLabTheme = () => {
    if (typeof document === 'undefined') {
        return 'light'; // Default in SSR/non-browser
    }
    // Check for JupyterLab theme attribute on body or html
    const themeLight = document.body.getAttribute('data-jp-theme-light') === 'true' ||
        document.documentElement.getAttribute('data-jp-theme-light') === 'true';
    return themeLight ? 'light' : 'dark';
};
// Theme provider component
const ThemeProvider = ({ children, commands }) => {
    // Get initial theme mode from localStorage or default to system
    const [themeMode, _setThemeMode] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(() => {
        if (typeof window !== 'undefined') {
            const savedMode = localStorage.getItem('jupyt-theme-mode');
            return savedMode || 'system';
        }
        return 'system';
    });
    // Calculate the actual theme based on mode and JupyterLab/system preference
    const [currentTheme, setCurrentTheme] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(() => themeMode === 'system'
        ? getJupyterLabTheme()
        : themeMode);
    // New setThemeMode function that includes command execution
    const setThemeMode = async (mode) => {
        _setThemeMode(mode); // Update internal state
        // Save preference to localStorage
        if (typeof window !== 'undefined') {
            localStorage.setItem('jupyt-theme-mode', mode);
        }
        // Change JupyterLab theme if mode is light or dark
        if (mode === 'light' || mode === 'dark') {
            const targetTheme = mode === 'light' ? JUPYTERLAB_LIGHT_THEME : JUPYTERLAB_DARK_THEME;
            try {
                if (commands.hasCommand('apputils:change-theme')) {
                    await commands.execute('apputils:change-theme', {
                        theme: targetTheme
                    });
                    console.log(`Jupyt AI: Changed JupyterLab theme to ${targetTheme}`);
                }
                else {
                    console.warn('Jupyt AI: Command apputils:change-theme not found.');
                }
            }
            catch (error) {
                console.error(`Jupyt AI: Failed to change JupyterLab theme to ${targetTheme}:`, error);
            }
        }
    };
    // Update the theme when internal themeMode state changes
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        // Removed localStorage setting here, handled in setThemeMode
        // If theme is set to system, sync from JupyterLab's theme
        if (themeMode === 'system') {
            setCurrentTheme(getJupyterLabTheme());
        }
    }, [themeMode]); // Depends on internal themeMode
    // Listen for JupyterLab theme changes when in system mode
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (themeMode !== 'system' || typeof document === 'undefined') {
            return;
        }
        // Use MutationObserver to detect changes in JupyterLab theme attribute
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'attributes' &&
                    (mutation.attributeName === 'data-jp-theme-light' ||
                        mutation.attributeName === 'data-jp-theme-name')) {
                    const newJupyterLabTheme = getJupyterLabTheme();
                    // Always update the visual theme
                    setCurrentTheme(newJupyterLabTheme);
                    // Get the current setting value *before* potentially changing it
                    const currentSetting = themeMode; // Access the state variable directly
                    // If the setting is not 'system' and it mismatches the new theme,
                    // update the setting itself to reflect the change.
                    if (currentSetting !== 'system' &&
                        currentSetting !== newJupyterLabTheme) {
                        _setThemeMode(newJupyterLabTheme); // Update the state controlling the dropdown
                        // Also update localStorage to persist this externally triggered change
                        if (typeof window !== 'undefined') {
                            localStorage.setItem('jupyt-theme-mode', newJupyterLabTheme);
                        }
                        console.log(`Jupyt AI: Setting changed to ${newJupyterLabTheme} to match external JupyterLab theme change.`);
                    }
                }
            });
        });
        // Observe changes on body and html attributes
        observer.observe(document.body, { attributes: true });
        observer.observe(document.documentElement, { attributes: true });
        // Initial check in case the theme changed before observer was set up
        setCurrentTheme(getJupyterLabTheme());
        // Clean up observer on unmount or when mode changes
        return () => {
            observer.disconnect();
        };
    }, [themeMode]); // Re-run effect if themeMode changes
    // Create theme based on current mode
    const theme = (0,_theme__WEBPACK_IMPORTED_MODULE_1__.createAppTheme)(currentTheme);
    // Use the new setThemeMode in the context provider value
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ThemeContext.Provider, { value: { themeMode, setThemeMode, currentTheme } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_styles__WEBPACK_IMPORTED_MODULE_2__["default"], { theme: theme },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_3__["default"], null),
            children)));
};


/***/ }),

/***/ "./lib/theme.js":
/*!**********************!*\
  !*** ./lib/theme.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   createAppTheme: () => (/* binding */ createAppTheme),
/* harmony export */   darkThemeOptions: () => (/* binding */ darkThemeOptions),
/* harmony export */   getSystemThemePreference: () => (/* binding */ getSystemThemePreference),
/* harmony export */   lightThemeOptions: () => (/* binding */ lightThemeOptions)
/* harmony export */ });
/* harmony import */ var _mui_material_styles__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material/styles */ "./node_modules/@mui/material/esm/styles/createTheme.js");

// Helper function to read JupyterLab CSS variables
const getJupyterLabColor = (varName, fallback) => {
    if (typeof window === 'undefined' || !document) {
        return fallback;
    }
    // Try to get the color from JupyterLab CSS variables
    const computedStyle = window.getComputedStyle(document.documentElement);
    return computedStyle.getPropertyValue(varName).trim() || fallback;
};
// Light theme configuration that integrates with JupyterLab
const lightThemeOptions = {
    palette: {
        mode: 'light',
        primary: {
            main: getJupyterLabColor('--jp-brand-color1', '#1976d2')
        },
        secondary: {
            main: getJupyterLabColor('--jp-warn-color0', '#dc004e')
        },
        background: {
            default: getJupyterLabColor('--jp-layout-color0', '#f5f5f5'),
            paper: getJupyterLabColor('--jp-layout-color1', '#ffffff')
        },
        text: {
            primary: getJupyterLabColor('--jp-content-font-color0', '#212121'),
            secondary: getJupyterLabColor('--jp-content-font-color2', '#757575')
        },
        divider: getJupyterLabColor('--jp-border-color1', '#e0e0e0')
    },
    components: {
        MuiCssBaseline: {
            styleOverrides: {
                body: {
                    color: getJupyterLabColor('--jp-content-font-color0', '#212121'),
                    backgroundColor: 'transparent'
                }
            }
        }
    }
};
// Dark theme configuration that integrates with JupyterLab
const darkThemeOptions = {
    palette: {
        mode: 'dark',
        primary: {
            main: getJupyterLabColor('--jp-brand-color1', '#90caf9')
        },
        secondary: {
            main: getJupyterLabColor('--jp-warn-color0', '#f48fb1')
        },
        background: {
            default: getJupyterLabColor('--jp-layout-color0', '#121212'),
            paper: getJupyterLabColor('--jp-layout-color1', '#1e1e1e')
        },
        text: {
            primary: getJupyterLabColor('--jp-content-font-color0', '#e0e0e0'),
            secondary: getJupyterLabColor('--jp-content-font-color2', '#a0a0a0')
        },
        divider: getJupyterLabColor('--jp-border-color1', '#424242')
    },
    components: {
        MuiCssBaseline: {
            styleOverrides: {
                body: {
                    color: getJupyterLabColor('--jp-content-font-color0', '#e0e0e0'),
                    backgroundColor: 'transparent'
                }
            }
        }
    }
};
// Create theme based on the mode
const createAppTheme = (mode) => {
    return (0,_mui_material_styles__WEBPACK_IMPORTED_MODULE_0__["default"])(mode === 'light' ? lightThemeOptions : darkThemeOptions);
};
// Get system color scheme preference
const getSystemThemePreference = () => {
    if (typeof window !== 'undefined' && window.matchMedia) {
        return window.matchMedia('(prefers-color-scheme: dark)').matches
            ? 'dark'
            : 'light';
    }
    return 'light'; // Default to light if matchMedia is not available
};


/***/ }),

/***/ "./lib/types/cell-metadata.js":
/*!************************************!*\
  !*** ./lib/types/cell-metadata.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   APPROVED_OPERATION_METADATA_KEY: () => (/* binding */ APPROVED_OPERATION_METADATA_KEY),
/* harmony export */   PENDING_OPERATION_METADATA_KEY: () => (/* binding */ PENDING_OPERATION_METADATA_KEY)
/* harmony export */ });
/**
 * Key used to store pending operation metadata in a cell.
 */
const PENDING_OPERATION_METADATA_KEY = 'jupyt_pending_operation';
/**
 * Key used to store approved operation metadata in a cell.
 */
const APPROVED_OPERATION_METADATA_KEY = 'jupyt_approved_operation';


/***/ }),

/***/ "./lib/utils/cellOutputExtractor.js":
/*!******************************************!*\
  !*** ./lib/utils/cellOutputExtractor.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   extractTextOutputFromCell: () => (/* binding */ extractTextOutputFromCell)
/* harmony export */ });
/**
 * Extracts plain text output from a notebook cell, ignoring images/plots.
 * @param cell The notebook cell object
 * @returns Concatenated plain text output
 */
function extractTextOutputFromCell(cell) {
    if (!cell.outputs || !Array.isArray(cell.outputs)) {
        return '';
    }
    return cell.outputs
        .filter(output => output.output_type === 'stream' ||
        output.output_type === 'error' ||
        (output.output_type === 'execute_result' &&
            output.data &&
            typeof output.data['text/plain'] === 'string'))
        .map(output => {
        if (output.output_type === 'stream') {
            return output.text || '';
        }
        if (output.output_type === 'error') {
            return ((output.ename || '') + ': ' + (output.evalue || ''));
        }
        if (output.output_type === 'execute_result' &&
            output.data &&
            output.data['text/plain']) {
            return output.data['text/plain'];
        }
        return '';
    })
        .join('\n')
        .trim();
}


/***/ }),

/***/ "./lib/utils/chatUtils.js":
/*!********************************!*\
  !*** ./lib/utils/chatUtils.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   extractCellReferences: () => (/* binding */ extractCellReferences),
/* harmony export */   extractJsonFromContent: () => (/* binding */ extractJsonFromContent),
/* harmony export */   removeCellOperationTags: () => (/* binding */ removeCellOperationTags),
/* harmony export */   stripCodeBlockMarkers: () => (/* binding */ stripCodeBlockMarkers)
/* harmony export */ });
function extractCellReferences(text) {
    const cellRefs = text.match(/@cell(\d+)/g) || [];
    const cellNumbers = new Set(cellRefs.map(ref => parseInt(ref.replace('@cell', ''), 10)));
    const cleanQuery = text.replace(/@cell\d+\s*/g, '').trim();
    return { cleanQuery, cellNumbers };
}
// Utility to strip markdown code block markers from code
function stripCodeBlockMarkers(code) {
    // Remove triple backticks and optional language
    return code.replace(/^```[a-zA-Z]*\n?|```$/gm, '').trim();
}
// Helper to extract JSON object from a string containing text + JSON
function extractJsonFromContent(content) {
    const firstBrace = content.indexOf('{');
    const lastBrace = content.lastIndexOf('}');
    if (firstBrace !== -1 && lastBrace !== -1 && lastBrace > firstBrace) {
        const jsonStr = content.slice(firstBrace, lastBrace + 1);
        try {
            const json = JSON.parse(jsonStr);
            const rest = (content.slice(0, firstBrace) + content.slice(lastBrace + 1)).trim();
            return { json, rest };
        }
        catch (e) {
            // fallback: treat as plain text
        }
    }
    return { json: null, rest: content };
}
/**
 * Removes all <cell_operation>...</cell_operation> blocks from a string.
 */
function removeCellOperationTags(input) {
    return input
        .replace(/<cell_operation>[\s\S]*?<\/cell_operation>/g, '')
        .trim();
}


/***/ }),

/***/ "./lib/utils/notebook-state-extractor.js":
/*!***********************************************!*\
  !*** ./lib/utils/notebook-state-extractor.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   extractNotebookState: () => (/* binding */ extractNotebookState)
/* harmony export */ });
/**
 * Extracts the full notebook state in the format required by the agentic loop API.
 * @param notebookPanel The JupyterLab NotebookPanel instance
 * @returns INotebookState object containing all cells and notebook metadata
 */
function extractNotebookState(notebookPanel) {
    if (!notebookPanel || !notebookPanel.model) {
        return { cells: [], metadata: {} };
    }
    const notebook = notebookPanel.content;
    const model = notebookPanel.model;
    const cells = notebook.widgets.map((cellWidget, idx) => {
        var _a, _b;
        const cellModel = cellWidget.model;
        return {
            cell_id: cellModel.id,
            cell_type: cellModel.type,
            source: cellModel.sharedModel.getSource(),
            outputs: cellModel.type === 'code' && 'outputs' in cellModel
                ? ((_b = (_a = cellModel.outputs) === null || _a === void 0 ? void 0 : _a.toJSON) === null || _b === void 0 ? void 0 : _b.call(_a)) || []
                : [],
            cell_index: idx
        };
    });
    const metadata = model.sharedModel.getMetadata();
    return { cells, metadata };
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.c8f218e41fccddf2d48d.js.map