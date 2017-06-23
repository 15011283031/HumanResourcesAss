create view [dbo].[S_SYS_PUBLICUPDATE] AS
With extendMain as (
	Select * From PAYORGBUSINESSDATA 
		Where Groupid = ( 
			Select Groupid From Payextenddatagroup 
				where isdeleted=0 
				and GROUPNAME='���¹��ô�����ϸ'
		) 
)
,extendDetail AS (
	select * from PAYORGBUSINESSDATADETAIL 
		where itemid in ( 
			Select ITEMID From Payextenddatagroupitem 
				Where Groupid = ( 
					Select Groupid From Payextenddatagroup 
						where isdeleted=0 
						and GROUPNAME='���¹��ô�����ϸ'
				) 
				AND ITEMNAME in (
					Select ITEMNAME From Payextenddatagroupitem 
						Where Groupid = ( 
							Select Groupid From Payextenddatagroup 
								where isdeleted=0 
								and GROUPNAME='���¹��ô�����ϸ'
						)
				)
		)
)

select detail1.ITEMVALUE ���ô�������,detail2.ITEMVALUE ���ô�����,detail3.ITEMVALUE ���ô������� from extendMain
	left join extendDetail detail1 on extendMain.DATAID=detail1.DATAID and detail1.ITEMID = (Select ITEMID From Payextenddatagroupitem Where Groupid = ( Select Groupid From Payextenddatagroup where isdeleted=0 and GROUPNAME='���¹��ô�����ϸ') AND ITEMNAME='���ô�������')
	left join extendDetail detail2 on extendMain.DATAID=detail2.DATAID and detail2.ITEMID = (Select ITEMID From Payextenddatagroupitem Where Groupid = ( Select Groupid From Payextenddatagroup where isdeleted=0 and GROUPNAME='���¹��ô�����ϸ') AND ITEMNAME='���ô�����')
	left join extendDetail detail3 on extendMain.DATAID=detail3.DATAID and detail3.ITEMID = (Select ITEMID From Payextenddatagroupitem Where Groupid = ( Select Groupid From Payextenddatagroup where isdeleted=0 and GROUPNAME='���¹��ô�����ϸ') AND ITEMNAME='���ô�������')

GO


