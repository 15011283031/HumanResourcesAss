create view [dbo].[S_SYS_PUBLICUPDATE] AS
With extendMain as (
	Select * From PAYORGBUSINESSDATA 
		Where Groupid = ( 
			Select Groupid From Payextenddatagroup 
				where isdeleted=0 
				and GROUPNAME='更新公用代码明细'
		) 
)
,extendDetail AS (
	select * from PAYORGBUSINESSDATADETAIL 
		where itemid in ( 
			Select ITEMID From Payextenddatagroupitem 
				Where Groupid = ( 
					Select Groupid From Payextenddatagroup 
						where isdeleted=0 
						and GROUPNAME='更新公用代码明细'
				) 
				AND ITEMNAME in (
					Select ITEMNAME From Payextenddatagroupitem 
						Where Groupid = ( 
							Select Groupid From Payextenddatagroup 
								where isdeleted=0 
								and GROUPNAME='更新公用代码明细'
						)
				)
		)
)

select detail1.ITEMVALUE 公用代码名称,detail2.ITEMVALUE 公用代码编号,detail3.ITEMVALUE 公用代码类型 from extendMain
	left join extendDetail detail1 on extendMain.DATAID=detail1.DATAID and detail1.ITEMID = (Select ITEMID From Payextenddatagroupitem Where Groupid = ( Select Groupid From Payextenddatagroup where isdeleted=0 and GROUPNAME='更新公用代码明细') AND ITEMNAME='公用代码名称')
	left join extendDetail detail2 on extendMain.DATAID=detail2.DATAID and detail2.ITEMID = (Select ITEMID From Payextenddatagroupitem Where Groupid = ( Select Groupid From Payextenddatagroup where isdeleted=0 and GROUPNAME='更新公用代码明细') AND ITEMNAME='公用代码编号')
	left join extendDetail detail3 on extendMain.DATAID=detail3.DATAID and detail3.ITEMID = (Select ITEMID From Payextenddatagroupitem Where Groupid = ( Select Groupid From Payextenddatagroup where isdeleted=0 and GROUPNAME='更新公用代码明细') AND ITEMNAME='公用代码类型')

GO


