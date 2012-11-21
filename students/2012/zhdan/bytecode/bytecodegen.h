/*
 * codegen.h
 *
 *  Created on: Oct 29, 2012
 *      Author: user
 */

#ifndef CODEGEN_H_
#define CODEGEN_H_

#include "mathvm.h"
#include <string>
#include "astinfo.h"

namespace mathvm {

class CodeGenVisitor: public AstVisitor {

public:
	CodeGenVisitor(Code* code): _code(code){}
	~CodeGenVisitor();

	virtual void visitBinaryOpNode(BinaryOpNode* node);
	virtual void visitUnaryOpNode(UnaryOpNode* node);
	virtual void visitStringLiteralNode(StringLiteralNode* node);
	virtual void visitDoubleLiteralNode(DoubleLiteralNode* node);
	virtual void visitIntLiteralNode(IntLiteralNode* node);
	virtual void visitLoadNode(LoadNode* node);
	virtual void visitStoreNode(StoreNode* node);
	virtual void visitForNode(ForNode* node);
	virtual void visitWhileNode(WhileNode* node);
	virtual void visitIfNode(IfNode* node);
	virtual void visitBlockNode(BlockNode* node);
	virtual void visitFunctionNode(FunctionNode* node);
	virtual void visitReturnNode(ReturnNode* node);
	virtual void visitCallNode(CallNode* node);
	virtual void visitNativeCallNode(NativeCallNode* node);
	virtual void visitPrintNode(PrintNode* node);

private:
	const Code* _code;

	Bytecode* getCurrentBytecode();
	void load_string_const(const string& value);
	void load_double_const(double value);
	void load_int_const(int value);
	void load_var(const AstVar* var);
	void process_numbers_bin_op(VarType commonType, AstNode* left, AstNode* right, Instruction ifInt, Instruction ifDouble);
	void process_comprarision(AstNode* left, AstNode* right, Instruction comprassion);
	void process_logic_operation(AstNode* left, AstNode* right, Instruction operation);
	void convert_to_boolean(AstNode* node);
	Scope* get_curernt_scope();
	void set_current_scope(Scope* scope);
	int get_function_id(AstFunction* function);
};

}

#endif /* CODEGEN_H_ */