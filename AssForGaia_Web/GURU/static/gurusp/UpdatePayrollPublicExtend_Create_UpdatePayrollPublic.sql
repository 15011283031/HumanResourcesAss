CREATE PROCEDURE [dbo].[updatePayrollPublic] as
begin
insert into PAYPAYROLLPUBCODEITEM 
	(CODEID,ITEMID,ITEMNAME,ITEMORDER,ISSYSTEMCODE,ISDELETED,BUSINESSUNITID)
SELECT code.CODEID CODEID,NEWID() ITEMID,publicUpdate.���ô������� ITEMNAME,publicUpdate.���ô����� ITEMORDER,0 ISSYSTEMCODE,0 ISDELETED,0 BUSINESSUNITID
	FROM S_SYS_PUBLICUPDATE publicUpdate
	join PAYPAYROLLPUBLICCODE code on publicUpdate.���ô������� = code.CODENAME
	left join PAYPAYROLLPUBCODEITEM item on publicUpdate.���ô������� = item.ITEMNAME and code.CODEID=item.CODEID
	WHERE item.CODEID IS NULL;

update PAYPAYROLLPUBCODEITEM set ITEMORDER = publicUpdate.���ô����� --SELECT * 
	from S_SYS_PUBLICUPDATE publicUpdate
	join PAYPAYROLLPUBLICCODE code on publicUpdate.���ô������� = code.CODENAME
    join PAYPAYROLLPUBCODEITEM item on publicUpdate.���ô������� = item.ITEMNAME 
		and publicUpdate.���ô����� <> item.ITEMORDER and code.CODEID=item.CODEID
end

GO


