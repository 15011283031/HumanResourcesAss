CREATE PROCEDURE [dbo].[updatePayrollPublic] as
begin
insert into PAYPAYROLLPUBCODEITEM 
	(CODEID,ITEMID,ITEMNAME,ITEMORDER,ISSYSTEMCODE,ISDELETED,BUSINESSUNITID)
SELECT code.CODEID CODEID,NEWID() ITEMID,publicUpdate.公用代码名称 ITEMNAME,publicUpdate.公用代码编号 ITEMORDER,0 ISSYSTEMCODE,0 ISDELETED,0 BUSINESSUNITID
	FROM S_SYS_PUBLICUPDATE publicUpdate
	join PAYPAYROLLPUBLICCODE code on publicUpdate.公用代码类型 = code.CODENAME
	left join PAYPAYROLLPUBCODEITEM item on publicUpdate.公用代码名称 = item.ITEMNAME and code.CODEID=item.CODEID
	WHERE item.CODEID IS NULL;

update PAYPAYROLLPUBCODEITEM set ITEMORDER = publicUpdate.公用代码编号 --SELECT * 
	from S_SYS_PUBLICUPDATE publicUpdate
	join PAYPAYROLLPUBLICCODE code on publicUpdate.公用代码类型 = code.CODENAME
    join PAYPAYROLLPUBCODEITEM item on publicUpdate.公用代码名称 = item.ITEMNAME 
		and publicUpdate.公用代码编号 <> item.ITEMORDER and code.CODEID=item.CODEID
end

GO


